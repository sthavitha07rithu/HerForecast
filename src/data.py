from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


SYMPTOM_MAP = {
    "Very Low/Little": 0,
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Very High": 4,
}


@dataclass
class TaskFrame:
    features: pd.DataFrame
    target: pd.Series
    groups: pd.Series
    feature_columns: List[str]


def _normalize_text(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_")


def _to_numeric_severity(series: pd.Series) -> pd.Series:
    cleaned = series.astype(str).str.strip()
    return cleaned.map(SYMPTOM_MAP)


def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Normalize column names for mixed-source datasets.
    normalized = {c: _normalize_text(c) for c in df.columns}
    df = df.rename(columns=normalized)

    alias_map = {
        "phase": ["phase"],
        "estrogen": ["estrogen"],
        "pdg": ["pdg", "progesterone"],
        "lh": ["lh"],
        "rmssd_mean": ["rmssd_mean", "ppg_rmssd"],
        "wrist_temp_mean": ["wrist_temp_mean", "skin_temperature"],
        "oxygen_ratio_mean": ["oxygen_ratio_mean", "spo2"],
        "stress_score_mean": ["stress_score_mean", "gsr"],
        "day_in_study": ["day_in_study", "day_in_cycle"],
        "heart_rate": ["heart_rate"],
    }

    for canonical, aliases in alias_map.items():
        if canonical in df.columns:
            continue
        for alias in aliases:
            if alias in df.columns:
                df[canonical] = df[alias]
                break

    if "phase" in df.columns:
        df["phase"] = (
            df["phase"]
            .astype(str)
            .str.strip()
            .replace("nan", np.nan)
            .str.capitalize()
        )

    # Build participant IDs when dataset does not include one.
    if "id" not in df.columns:
        if "day_in_study" in df.columns:
            day = pd.to_numeric(df["day_in_study"], errors="coerce")
            rollover = (day < day.shift(1)).fillna(False)
            df["id"] = rollover.cumsum() + 1
        else:
            df["id"] = 1

    if "study_interval" not in df.columns:
        df["study_interval"] = 0

    return df


def enrich_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    required_cols = [
        "is_weekend",
        "lh",
        "estrogen",
        "pdg",
        "wrist_temp_max",
        "wrist_temp_min",
        "oxygen_ratio_max",
        "oxygen_ratio_min",
        "id",
        "day_in_study",
        "rmssd_mean",
        "wrist_temp_mean",
    ]
    for col in required_cols:
        if col not in data.columns:
            data[col] = np.nan

    data["is_weekend"] = data["is_weekend"].astype(str).str.lower().map(
        {"true": 1, "false": 0}
    )
    data["is_weekend"] = data["is_weekend"].fillna(0)

    # Hormone and physiological ratio features.
    eps = 1e-6
    data["lh_estrogen_ratio"] = data["lh"] / (data["estrogen"] + eps)
    data["pdg_estrogen_ratio"] = data["pdg"] / (data["estrogen"] + eps)
    data["temp_range"] = data["wrist_temp_max"] - data["wrist_temp_min"]
    data["oxygen_range"] = data["oxygen_ratio_max"] - data["oxygen_ratio_min"]

    # Group-aware temporal features.
    data = data.sort_values(["id", "day_in_study"]).reset_index(drop=True)
    group = data.groupby("id", dropna=False)
    for col in ["lh", "estrogen", "pdg", "rmssd_mean", "wrist_temp_mean"]:
        if col in data.columns:
            data[f"{col}_delta_1d"] = group[col].diff(1)
            data[f"{col}_roll3"] = group[col].transform(
                lambda s: s.rolling(3, min_periods=1).mean()
            )
            data[f"{col}_roll7"] = group[col].transform(
                lambda s: s.rolling(7, min_periods=1).mean()
            )
    return data


def build_mood_label(df: pd.DataFrame) -> pd.Series:
    fatigue = _to_numeric_severity(df.get("fatigue", pd.Series(index=df.index)))
    stress = _to_numeric_severity(df.get("stress", pd.Series(index=df.index)))
    moodswing = _to_numeric_severity(df.get("moodswing", pd.Series(index=df.index)))
    sleepissue = _to_numeric_severity(df.get("sleepissue", pd.Series(index=df.index)))
    exertion = pd.to_numeric(df.get("exertion_points_mean"), errors="coerce")
    sleep_points = pd.to_numeric(df.get("sleep_points_mean"), errors="coerce")

    burden = (
        fatigue.fillna(1.5) * 0.35
        + stress.fillna(1.5) * 0.25
        + moodswing.fillna(1.0) * 0.20
        + sleepissue.fillna(1.0) * 0.20
    )

    mood = pd.Series("neutral", index=df.index, dtype="object")
    mood = mood.mask((burden >= 2.8) | (sleep_points < 45), "fatigued")
    mood = mood.mask((burden >= 2.3) & (mood == "neutral"), "tired")
    mood = mood.mask(
        (burden <= 1.2) & (exertion > 40) & (sleep_points > 60), "motivated"
    )
    mood = mood.mask((burden <= 1.4) & (sleep_points > 55) & (mood == "neutral"), "energetic")
    return mood


def build_phase_task(df: pd.DataFrame) -> TaskFrame:
    data = enrich_features(df)
    data = data.dropna(subset=["phase"]).copy()
    data = data.sort_values(["id", "day_in_study"]).reset_index(drop=True)
    data["phase_prev_day"] = data.groupby("id", dropna=False)["phase"].shift(1)

    excluded = {"phase", "id"}
    feature_columns = [c for c in data.columns if c not in excluded]
    features = data[feature_columns]
    target = data["phase"].astype(str)
    groups = data["id"].astype(str)
    return TaskFrame(features=features, target=target, groups=groups, feature_columns=feature_columns)


def build_mood_task(df: pd.DataFrame) -> TaskFrame:
    data = enrich_features(df)
    data["mood_today"] = build_mood_label(data)
    data = data.sort_values(["id", "day_in_study"]).reset_index(drop=True)
    data["mood_next_day"] = data.groupby("id", dropna=False)["mood_today"].shift(-1)
    data = data.dropna(subset=["mood_next_day"]).copy()

    excluded = {"mood_today", "mood_next_day", "phase", "id"}
    feature_columns = [c for c in data.columns if c not in excluded]
    features = data[feature_columns]
    target = data["mood_next_day"].astype(str)
    groups = data["id"].astype(str)
    return TaskFrame(features=features, target=target, groups=groups, feature_columns=feature_columns)


def dataset_summary(df: pd.DataFrame) -> Dict[str, object]:
    missing = (df.isna().mean() * 100).sort_values(ascending=False).head(12).round(2)
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "phase_distribution": df["phase"].value_counts(dropna=False).to_dict(),
        "top_missing_pct": missing.to_dict(),
    }

