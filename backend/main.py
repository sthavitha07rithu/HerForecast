from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import pandas as pd
import io
import traceback

from .model_loader import load_model, get_pipeline, get_feature_columns
from .schemas import PredictRequest, PredictResponse, HealthResponse, ModelInfoResponse
from .prediction_service import preprocess_data, predict_phase


# ----------------------------
# Application Lifespan
# ----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_model()
        print("Model loaded successfully at startup.")
    except Exception as e:
        print(f"Model failed to load: {e}")
        raise e
    yield


app = FastAPI(
    title="Inner Weather Backend",
    description="API for menstrual phase prediction using wearable data",
    version="1.0.0",
    lifespan=lifespan
)

# ----------------------------
# CORS (allow frontend access)
# ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Root (Serve Frontend)
# ----------------------------

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


# ----------------------------
# Health Check
# ----------------------------

@app.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        model_loaded = get_pipeline() is not None
        return HealthResponse(status="ok", model_loaded=model_loaded)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Single Prediction Endpoint
# ----------------------------

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    try:
        wearable_data = request.wearable_data.dict()
        hormone_data = request.hormone_data.dict()
        day_in_cycle = request.day_in_cycle

        feature_dict = preprocess_data(
            wearable_data=wearable_data,
            hormone_data=hormone_data,
            day_in_cycle=day_in_cycle
        )

        result = predict_phase(feature_dict)

        return PredictResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Prediction failed")


# ----------------------------
# CSV Upload Prediction
# ----------------------------

@app.post("/predict-csv")
async def predict_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        pipeline = get_pipeline()
        feature_columns = get_feature_columns()

        # Ensure all required features exist
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0.0

        df = df[feature_columns]

        predictions = pipeline.predict(df)

        result_df = df.copy()
        result_df["predicted_phase"] = predictions

        return result_df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------
# Model Info
# ----------------------------

@app.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    try:
        feature_columns = get_feature_columns()
        return ModelInfoResponse(
            model_name="Inner Weather Synthetic Phase Model",
            expected_features=feature_columns
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Run Locally
# ----------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)