from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from src.config import SEED
from src.preprocessing import build_preprocessor


@dataclass
class SplitData:
    X_train: object
    X_test: object
    y_train: np.ndarray
    y_test: np.ndarray
    groups_train: object
    groups_test: object


def split_group_holdout(X, y, groups, test_size: float = 0.2) -> SplitData:
    unique_groups = groups.astype(str).nunique()
    if unique_groups < 2:
        n = len(X)
        cutoff = int(n * (1 - test_size))
        cutoff = max(1, min(cutoff, n - 1))
        train_idx = np.arange(0, cutoff)
        test_idx = np.arange(cutoff, n)
    else:
        splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=SEED)
        train_idx, test_idx = next(splitter.split(X, y, groups=groups))
    return SplitData(
        X_train=X.iloc[train_idx].copy(),
        X_test=X.iloc[test_idx].copy(),
        y_train=y.iloc[train_idx].copy(),
        y_test=y.iloc[test_idx].copy(),
        groups_train=groups.iloc[train_idx].copy(),
        groups_test=groups.iloc[test_idx].copy(),
    )


def _candidate_models():
    return {
        "logistic_regression": (
            LogisticRegression(max_iter=1500, class_weight="balanced"),
            {
                "model__C": np.logspace(-2, 2, 10),
            },
        ),
        "random_forest": (
            RandomForestClassifier(
                random_state=SEED, n_estimators=300, class_weight="balanced_subsample"
            ),
            {
                "model__max_depth": [6, 8, 12, 16, None],
                "model__min_samples_split": [2, 5, 8, 12],
                "model__min_samples_leaf": [1, 2, 4],
            },
        ),
        "hist_gradient_boosting": (
            HistGradientBoostingClassifier(random_state=SEED),
            {
                "model__learning_rate": [0.03, 0.05, 0.08, 0.1],
                "model__max_depth": [4, 6, 8, None],
                "model__max_iter": [150, 250, 350],
                "model__min_samples_leaf": [20, 40, 80],
            },
        ),
    }


def train_best_model(X_train, y_train, groups_train) -> Tuple[str, Pipeline, Dict[str, float]]:
    preprocessor = build_preprocessor(X_train)
    best_name = ""
    best_pipe = None
    best_cv = -1.0
    cv_scores = {}

    for name, (model, params) in _candidate_models().items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])
        search = RandomizedSearchCV(
            estimator=pipe,
            param_distributions=params,
            n_iter=8,
            scoring="accuracy",
            cv=3,
            n_jobs=-1,
            random_state=SEED,
            verbose=0,
        )
        search.fit(X_train, y_train)
        cv_scores[name] = float(search.best_score_)
        if search.best_score_ > best_cv:
            best_cv = float(search.best_score_)
            best_name = name
            best_pipe = search.best_estimator_

    assert best_pipe is not None, "No model was trained."
    return best_name, best_pipe, cv_scores


def evaluate_classifier(model, X_test, y_test) -> Dict[str, object]:
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_test, y_pred, average="weighted")),
        "precision_weighted": float(
            precision_score(y_test, y_pred, average="weighted", zero_division=0)
        ),
        "recall_weighted": float(
            recall_score(y_test, y_pred, average="weighted", zero_division=0)
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
    }

    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba(X_test)
            if probs.shape[1] == 2:
                metrics["roc_auc_ovr"] = float(roc_auc_score(y_test, probs[:, 1]))
            else:
                metrics["roc_auc_ovr"] = float(
                    roc_auc_score(y_test, probs, multi_class="ovr", average="macro")
                )
        except Exception:
            metrics["roc_auc_ovr"] = None
    else:
        metrics["roc_auc_ovr"] = None
    return metrics


def build_feature_importance_table(model: Pipeline, top_n: int = 15) -> list[dict]:
    classifier = model.named_steps["model"]
    preprocessor = model.named_steps["preprocessor"]
    feature_names = preprocessor.get_feature_names_out().tolist()

    if hasattr(classifier, "feature_importances_"):
        importances = classifier.feature_importances_
    elif hasattr(classifier, "coef_"):
        importances = np.mean(np.abs(classifier.coef_), axis=0)
    else:
        return []

    top_idx = np.argsort(importances)[::-1][:top_n]
    return [
        {"feature": feature_names[idx], "importance": float(importances[idx])}
        for idx in top_idx
    ]


def encode_target(y):
    enc = LabelEncoder()
    y_encoded = enc.fit_transform(y)
    return enc, y_encoded

