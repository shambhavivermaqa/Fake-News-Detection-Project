"""Loads the trained pipeline once and exposes a simple predict() function."""

from functools import lru_cache

import joblib
import numpy as np

from src import config
from src.preprocess import build_input_text


class ModelNotTrainedError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _load_pipeline():
    if not (config.MODEL_PATH.exists() and config.VECTORIZER_PATH.exists()):
        raise ModelNotTrainedError(
            "No trained model found. Run 'python -m src.train' first "
            "(see README.md 'Train the model')."
        )
    vectorizer = joblib.load(config.VECTORIZER_PATH)
    model = joblib.load(config.MODEL_PATH)
    return vectorizer, model


def _confidence(model, X) -> float:
    if hasattr(model, "predict_proba"):
        return float(np.max(model.predict_proba(X)))
    if hasattr(model, "decision_function"):
        score = model.decision_function(X)[0]
        return float(1 / (1 + np.exp(-abs(score))))
    return 1.0


def predict(title: str, text: str) -> dict:
    """Predict FAKE/REAL for a given article title + body."""
    vectorizer, model = _load_pipeline()
    cleaned = build_input_text(title, text)
    if not cleaned:
        raise ValueError("Provide a non-empty title or article text.")

    X = vectorizer.transform([cleaned])
    label = model.predict(X)[0]
    confidence = _confidence(model, X)

    return {
        "label": label,
        "confidence": round(confidence * 100, 2),
        "cleaned_word_count": len(cleaned.split()),
    }
