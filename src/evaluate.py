"""Plotting helpers used to generate the figures under reports/figures."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay

from src import config

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#1a1a1a",
    "text.color": "#1a1a1a",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.25,
})

PRIMARY = "#2563eb"
ACCENT = "#dc2626"
PALETTE = ["#2563eb", "#0d9488", "#dc2626", "#7c3aed", "#ea580c"]


def _save(fig, name: str):
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.FIGURES_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def plot_confusion_matrix(y_true, y_pred, labels=config.LABELS, name="confusion_matrix.png"):
    fig, ax = plt.subplots(figsize=(5, 4.5))
    disp = ConfusionMatrixDisplay.from_predictions(
        y_true, y_pred, labels=labels, cmap="Blues", colorbar=False, ax=ax
    )
    ax.set_title("Confusion Matrix — Best Model", fontsize=13, fontweight="bold")
    return _save(fig, name)


def plot_roc_curve(y_true_binary, y_score, name="roc_curve.png"):
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    RocCurveDisplay.from_predictions(y_true_binary, y_score, ax=ax, color=PRIMARY)
    ax.plot([0, 1], [0, 1], linestyle="--", color="#999999", linewidth=1)
    ax.set_title("ROC Curve — Best Model", fontsize=13, fontweight="bold")
    return _save(fig, name)


def plot_model_comparison(results: dict, name="model_comparison.png"):
    models = list(results.keys())
    metrics = ["accuracy", "precision", "recall", "f1"]
    x = np.arange(len(models))
    width = 0.2

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, metric in enumerate(metrics):
        values = [results[m][metric] for m in models]
        ax.bar(x + i * width, values, width, label=metric.capitalize(), color=PALETTE[i])

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, rotation=10)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title("Model Comparison on Held-Out Test Set", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", ncol=2, fontsize=9)
    return _save(fig, name)


def plot_class_distribution(df, name="class_distribution.png"):
    counts = df["label"].value_counts()
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ax.bar(counts.index, counts.values, color=[ACCENT, PRIMARY])
    for i, v in enumerate(counts.values):
        ax.text(i, v + 20, str(v), ha="center", fontweight="bold")
    ax.set_title("Class Distribution", fontsize=13, fontweight="bold")
    ax.set_ylabel("Number of Articles")
    return _save(fig, name)


def plot_text_length_distribution(df, name="text_length_distribution.png"):
    lengths = df["clean_text"].str.split().apply(len)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(lengths, bins=40, color=PRIMARY, alpha=0.85)
    ax.set_title("Article Length Distribution (words)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Word count")
    ax.set_ylabel("Number of articles")
    return _save(fig, name)


def plot_top_features(vectorizer, model, top_n=20, name="top_predictive_words.png"):
    if not hasattr(model, "coef_"):
        return None
    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = model.coef_.ravel()

    top_fake_idx = np.argsort(coefs)[:top_n]
    top_real_idx = np.argsort(coefs)[-top_n:]

    fig, axes = plt.subplots(1, 2, figsize=(11, 6), sharex=False)
    axes[0].barh(feature_names[top_fake_idx], coefs[top_fake_idx], color=ACCENT)
    axes[0].set_title("Top words → FAKE", fontsize=12, fontweight="bold")
    axes[1].barh(feature_names[top_real_idx], coefs[top_real_idx], color=PRIMARY)
    axes[1].set_title("Top words → REAL", fontsize=12, fontweight="bold")
    fig.suptitle("Most Predictive Words (Model Coefficients)", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return _save(fig, name)
