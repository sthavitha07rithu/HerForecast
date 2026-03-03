from __future__ import annotations

from typing import Dict

import joblib
import numpy as np
import pandas as pd

from src.config import MOOD_ARTIFACT, PHASE_ARTIFACT
from src.data import enrich_features


FRIENDLY_MESSAGES = {
    "fatigued": "You might want to rest well today. Give yourself some me-time and recharge.",
    "tired": "A gentler pace could help today. Hydrate, breathe, and take short breaks.",
    "energetic": "Your energy looks strong today. A good day to do something you enjoy.",
    "motivated": "You may be in a focused flow today. Channel it into one meaningful win.",
    "neutral": "Today looks balanced. Keep a steady routine and be kind to yourself.",
}


def _uncertainty_message(base_msg: str) -> str:
    return f"{base_msg} We are less certain today, so listen to your body and adjust gently."


class Predictor:
    def __init__(self):
        self.phase_model = joblib.load(PHASE_ARTIFACT)
        self.mood_model = joblib.load(MOOD_ARTIFACT)
        self.phase_columns = list(self.phase_model.feature_names_in_)
        self.mood_columns = list(self.mood_model.feature_names_in_)

    def predict(self, payload: Dict) -> Dict:
        row = pd.DataFrame([payload])
        engineered = enrich_features(row)
        phase_input = self._align_columns(engineered, self.phase_columns)
        mood_input = self._align_columns(engineered, self.mood_columns)

        phase_pred = self.phase_model.predict(phase_input)[0]
        mood_pred = self.mood_model.predict(mood_input)[0]

        phase_conf = self._confidence(self.phase_model, phase_input)
        mood_conf = self._confidence(self.mood_model, mood_input)

        message = FRIENDLY_MESSAGES.get(str(mood_pred), FRIENDLY_MESSAGES["neutral"])
        if mood_conf < 0.6:
            message = _uncertainty_message(message)

        return {
            "phase": str(phase_pred),
            "phase_confidence": round(phase_conf, 4),
            "mood": str(mood_pred),
            "mood_confidence": round(mood_conf, 4),
            "friendly_message": message,
            "disclaimer": "This is wellness guidance, not medical advice.",
        }

    @staticmethod
    def _confidence(model, row) -> float:
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(row)[0]
            return float(probs.max())
        return 0.5

    @staticmethod
    def _align_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        aligned = df.copy()
        for col in columns:
            if col not in aligned.columns:
                aligned[col] = np.nan
        return aligned[columns]

