import os
import joblib
from typing import List, Any

# Global variables to store loaded model components
pipeline: Any = None
feature_columns: List[str] = []
label_classes: List[str] = []


def load_model(model_filename: str = "phase_model.joblib") -> None:
    """
    Load the scikit-learn pipeline and metadata from the joblib file.
    This should be called once at application startup.
    """
    global pipeline, feature_columns, label_classes

    try:
        # Get absolute path to this file's directory (backend/)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct full path to model file
        model_path = os.path.join(base_dir, model_filename)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        model_data = joblib.load(model_path)

        pipeline = model_data["pipeline"]
        feature_columns = model_data["feature_columns"]
        label_classes = model_data["label_classes"]

        print(f"Model loaded successfully from: {model_path}")

    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")


def get_pipeline():
    """Return the loaded pipeline."""
    if pipeline is None:
        raise RuntimeError("Model not loaded. Call load_model() first.")
    return pipeline


def get_feature_columns():
    """Return the expected feature columns."""
    if not feature_columns:
        raise RuntimeError("Model not loaded. Call load_model() first.")
    return feature_columns


def get_label_classes():
    """Return the label classes."""
    if not label_classes:
        raise RuntimeError("Model not loaded. Call load_model() first.")
    return label_classes
