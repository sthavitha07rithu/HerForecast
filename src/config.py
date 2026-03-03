from pathlib import Path

SEED = 42
DATA_PATH = Path("data/synthetic_women_cycle_data.csv")
MODEL_DIR = Path("models")
PHASE_ARTIFACT = MODEL_DIR / "phase_model.joblib"
MOOD_ARTIFACT = MODEL_DIR / "mood_model.joblib"
REPORT_PATH = MODEL_DIR / "evaluation_report.md"
METRICS_JSON = MODEL_DIR / "metrics.json"
