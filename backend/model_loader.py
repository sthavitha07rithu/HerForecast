import sys
import os
import joblib
from typing import List, Any
from sklearn.pipeline import Pipeline

# --- FIX FOR LEGACY PICKLE NAMESPACE (src -> backend.src) ---

import backend.src as backend_src
import backend.src.preprocessing as preprocessing
import backend.src.data as data
import backend.src.config as config
import backend.src.modeling as modeling

sys.modules["src"] = backend_src
sys.modules["src.preprocessing"] = preprocessing
sys.modules["src.data"] = data
sys.modules["src.config"] = config
sys.modules["src.modeling"] = modeling

# -------------------------------------------------------------

pipeline: Any = None
feature_columns: List[str] = []
label_classes: List[str] = []


def load_model(model_filename: str = "phase_model.joblib") -> None:
    global pipeline, feature_columns, label_classes

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, model_filename)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        model_data = joblib.load(model_path)

        # Case 1: Saved as dict with metadata
        if isinstance(model_data, dict):
            pipeline = model_data.get("pipeline")
            feature_columns = model_data.get("feature_columns", [])
            label_classes = model_data.get("label_classes", [])

        # Case 2: Saved directly as sklearn Pipeline
        elif isinstance(model_data, Pipeline):
            pipeline = model_data
            feature_columns = []   # Not available
            label_classes = []

        else:
            raise ValueError("Unsupported model file format.")

        if pipeline is None:
            raise ValueError("Pipeline could not be loaded.")

        print(f"Model loaded successfully from: {model_path}")

    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")


def get_pipeline():
    if pipeline is None:
        raise RuntimeError("Model not loaded.")
    return pipeline


def get_feature_columns():
    return feature_columns


def get_label_classes():
    return label_classes
