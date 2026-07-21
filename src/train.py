"""Trains and compares several classifiers, then persists the best pipeline.

Run with:  python -m src.train
"""

import json
import time

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from src import config, evaluate
from src.data_loader import load_or_create_splits

CANDIDATE_MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0),
    "Passive Aggressive": PassiveAggressiveClassifier(max_iter=1000, random_state=config.RANDOM_STATE),
    "Linear SVM": LinearSVC(max_iter=5000),
    "Multinomial Naive Bayes": MultinomialNB(),
}


def _binary(labels):
    return np.array([1 if l == "REAL" else 0 for l in labels])


def train_and_select_best():
    print("Loading dataset and building train/test split...")
    train_df, test_df = load_or_create_splits()
    print(f"  train: {len(train_df)} rows | test: {len(test_df)} rows")

    print("Fitting TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=config.TFIDF_MAX_FEATURES,
        ngram_range=config.TFIDF_NGRAM_RANGE,
        stop_words="english",
    )
    X_train = vectorizer.fit_transform(train_df["clean_text"])
    X_test = vectorizer.transform(test_df["clean_text"])
    y_train, y_test = train_df["label"].values, test_df["label"].values

    results = {}
    fitted_models = {}
    print("Training candidate models...")
    for name, model in CANDIDATE_MODELS.items():
        t0 = time.time()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        elapsed = time.time() - t0

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, pos_label="REAL"),
            "recall": recall_score(y_test, y_pred, pos_label="REAL"),
            "f1": f1_score(y_test, y_pred, pos_label="REAL"),
            "train_seconds": round(elapsed, 3),
        }
        results[name] = metrics
        fitted_models[name] = model
        print(f"  {name:<26} acc={metrics['accuracy']:.4f}  f1={metrics['f1']:.4f}  ({elapsed:.2f}s)")

    best_name = max(results, key=lambda n: results[n]["f1"])
    best_model = fitted_models[best_name]
    print(f"\nBest model: {best_name} (f1={results[best_name]['f1']:.4f})")

    y_pred_best = best_model.predict(X_test)

    print("Generating figures...")
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    evaluate.plot_class_distribution(train_df)
    evaluate.plot_text_length_distribution(train_df)
    evaluate.plot_model_comparison(results)
    evaluate.plot_confusion_matrix(y_test, y_pred_best)
    evaluate.plot_top_features(vectorizer, best_model)

    if hasattr(best_model, "decision_function"):
        scores = best_model.decision_function(X_test)
        evaluate.plot_roc_curve(_binary(y_test), scores)
        auc = roc_auc_score(_binary(y_test), scores)
        results[best_name]["roc_auc"] = auc

    print("Saving model artifacts...")
    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, config.VECTORIZER_PATH)
    joblib.dump(best_model, config.MODEL_PATH)

    metrics_payload = {
        "best_model": best_name,
        "dataset_size": int(len(train_df) + len(test_df)),
        "train_size": int(len(train_df)),
        "test_size": int(len(test_df)),
        "tfidf_max_features": config.TFIDF_MAX_FEATURES,
        "tfidf_ngram_range": list(config.TFIDF_NGRAM_RANGE),
        "results": results,
    }
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"\nSaved model      -> {config.MODEL_PATH}")
    print(f"Saved vectorizer -> {config.VECTORIZER_PATH}")
    print(f"Saved metrics    -> {config.METRICS_PATH}")
    print(f"Saved figures    -> {config.FIGURES_DIR}")
    return metrics_payload


if __name__ == "__main__":
    train_and_select_best()
