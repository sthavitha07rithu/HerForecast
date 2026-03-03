import numpy as np
import pandas as pd
from typing import Dict, Any
from .model_loader import get_pipeline, get_feature_columns, get_label_classes
from .mood_mapper import get_mood_from_phase


def preprocess_data(
    wearable_data: Dict[str, float],
    hormone_data: Dict[str, float],
    day_in_cycle: int
) -> Dict[str, Any]:
    """
    Preprocess the input data into a feature dictionary aligned with the model's expectations.
    """

    cycle_sin_28 = np.sin(2 * np.pi * day_in_cycle / 28)
    cycle_cos_28 = np.cos(2 * np.pi * day_in_cycle / 28)

    stress_score_mean = wearable_data.get("gsr_mean", 0.0)

    feature_dict = {
        "day_in_study": day_in_cycle,
        "cycle_sin_28": cycle_sin_28,
        "cycle_cos_28": cycle_cos_28,
        "rmssd_mean": wearable_data.get("ppg_rmssd", 0.0),
        "stress_score_mean": stress_score_mean,
        "wrist_temp_mean": wearable_data.get("skin_temp", 0.0),
        "lh": None,
        "estrogen": hormone_data.get("estrogen", 0.0),
        "pdg": hormone_data.get("progesterone", 0.0)
    }

    return feature_dict


def predict_phase(feature_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run inference using the loaded pipeline and return prediction results.
    """

    pipeline = get_pipeline()
    feature_columns = get_feature_columns()
    label_classes = get_label_classes()

    df = pd.DataFrame([feature_dict])

    # Align columns only if metadata exists
    if feature_columns:
        df = df.reindex(columns=feature_columns)

    prediction = pipeline.predict(df)[0]

    # --- Safe probability handling ---
    probabilities = None
    if hasattr(pipeline, "predict_proba"):
        try:
            probabilities = pipeline.predict_proba(df)[0]
        except Exception:
            probabilities = None

    # --- Resolve class labels ---
    classes = None

    if label_classes:
        classes = label_classes
    elif hasattr(pipeline, "classes_"):
        classes = pipeline.classes_
    elif hasattr(pipeline, "named_steps"):
        last_step = list(pipeline.named_steps.values())[-1]
        classes = getattr(last_step, "classes_", None)

    # --- Build probability dictionary safely ---
    if probabilities is not None and classes is not None:
        prob_dict = {
            str(label): float(prob)
            for label, prob in zip(classes, probabilities)
        }
        confidence = float(max(probabilities))
    else:
        prob_dict = {}
        confidence = 1.0

    mood = get_mood_from_phase(prediction)

    return {
        "predicted_phase": prediction,
        "predicted_mood": mood,
        "confidence": confidence,
        "probabilities": prob_dict
    }
