# Fake News Detection using Machine Learning

A full-stack, locally-runnable machine learning application that classifies news articles as **REAL** or **FAKE** using classical NLP (TF-IDF) and classical ML classifiers, served through a Flask web app with a clean, professional UI.

> Trained and evaluated on a real-world, labelled dataset of 6,300+ news articles. Best model: **Linear SVM**, achieving **93.66% accuracy** and **0.982 ROC-AUC** on a held-out test set.

---

## Table of Contents

- [Overview](#overview)
- [Live Demo (Local)](#live-demo-local)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Results](#results)
- [Setup Instructions](#setup-instructions)
- [Execution Guide](#execution-guide)
- [Web Application](#web-application)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Limitations & Disclaimer](#limitations--disclaimer)
- [Future Improvements](#future-improvements)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## Overview

Misinformation spreads faster than fact-checkers can respond. This project demonstrates a practical, explainable, end-to-end ML system for triaging news content:

1. **Data pipeline** — loads, cleans, and deduplicates a labelled news dataset.
2. **Model training** — trains and compares 4 classical ML classifiers, automatically selecting the best by F1 score.
3. **Evaluation & reporting** — generates accuracy/precision/recall/F1/ROC metrics and 6 diagnostic charts.
4. **Web application** — a Flask app that serves live predictions and a full model transparency/stats dashboard, running entirely on `localhost` (no external API calls, no cloud dependency).

## Live Demo (Local)

Once set up (see [Setup Instructions](#setup-instructions)), the app runs at:

```
http://127.0.0.1:5000
```

- **`/`** — paste a headline/article and get an instant REAL/FAKE prediction with a confidence score.
- **`/about`** — model comparison table, dataset statistics, and all evaluation charts.

## Project Structure

```
Fake-News-Detection-ML/
├── app/                        # Flask web application
│   ├── __init__.py             # app factory + routes
│   ├── static/
│   │   ├── css/style.css       # UI styling
│   │   └── js/main.js          # AJAX prediction form logic
│   └── templates/
│       ├── base.html
│       ├── index.html          # detector page
│       ├── about.html          # stats & metrics dashboard
│       └── 404.html
├── src/                        # ML pipeline (importable package)
│   ├── config.py               # paths & hyperparameters
│   ├── preprocess.py           # text cleaning
│   ├── data_loader.py          # dataset loading + train/test split
│   ├── train.py                # trains & compares models, saves best
│   ├── evaluate.py             # figure generation (matplotlib)
│   └── predict.py              # inference used by the web app
├── dataset/
│   ├── raw/                    # original dataset (fake_or_real_news.csv)
│   └── processed/               # generated train/test CSV splits
├── models/                      # saved TF-IDF vectorizer + trained model (.joblib)
├── reports/
│   ├── metrics.json             # full evaluation results
│   └── figures/                 # confusion matrix, ROC curve, comparisons, etc.
├── notebooks/                    # optional exploratory analysis
├── tests/                        # pytest unit tests
├── run.py                        # entry point — starts the Flask dev server
├── requirements.txt
├── conftest.py
├── .gitignore
└── README.md
```

## Dataset

This project uses the **"Fake or Real News"** dataset (originally curated for a well-known NLP fake-news classification benchmark; distributed via [lutzhamel/fake-news](https://github.com/lutzhamel/fake-news)).

| Property | Value |
|---|---|
| Total articles | 6,335 |
| Columns | `id`, `title`, `text`, `label` |
| Classes | `FAKE`, `REAL` (near-perfectly balanced: 3,164 / 3,171) |
| Missing values | None |

The raw file lives at `dataset/raw/fake_or_real_news.csv`. If you need to re-download it:

```bash
curl -L "https://raw.githubusercontent.com/lutzhamel/fake-news/master/data/fake_or_real_news.csv" -o dataset/raw/fake_or_real_news.csv
```

`src/data_loader.py` cleans the data (drops nulls/duplicates, normalizes labels) and creates a stratified 80/20 train/test split, cached under `dataset/processed/`.

## Machine Learning Pipeline

**Text preprocessing** (`src/preprocess.py`)
- Lowercasing, URL/HTML stripping, punctuation & digit removal, whitespace normalization.
- Title is concatenated with the body (title weighted 2x) before vectorization.

**Feature extraction**
- `TfidfVectorizer`: unigrams + bigrams, up to 50,000 features, English stop-words removed.

**Model selection** — 4 candidates are trained and evaluated on the same held-out test set; the best F1-scorer is automatically saved:

| Model |
|---|
| Logistic Regression |
| Passive Aggressive Classifier |
| Linear SVM ⭐ (selected) |
| Multinomial Naive Bayes |

**Artifacts produced** (`python -m src.train`):
- `models/tfidf_vectorizer.joblib`, `models/fake_news_model.joblib`
- `reports/metrics.json` — full metrics for every candidate model
- `reports/figures/*.png` — 6 evaluation charts

## Results

Metrics on the held-out test set (`reports/metrics.json`), most recent training run:

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.9200 | 0.9387 | 0.8986 | 0.9182 |
| Passive Aggressive | 0.9350 | 0.9420 | 0.9271 | 0.9345 |
| **Linear SVM (best)** | **0.9366** | **0.9480** | **0.9239** | **0.9358** |
| Multinomial Naive Bayes | 0.8914 | 0.8509 | 0.9493 | 0.8974 |

ROC-AUC (best model): **0.9818**

![Model Comparison](reports/figures/model_comparison.png)
![Confusion Matrix](reports/figures/confusion_matrix.png)

More charts (ROC curve, class distribution, article length distribution, top predictive words) are available in `reports/figures/` and rendered live on the app's `/about` page.

## Setup Instructions

**Prerequisites:** Python 3.10+ and `pip`.

```bash
# 1. Navigate into the project folder
cd Fake-News-Detection-ML

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Execution Guide

**Step 1 — Train the model** (skip if `models/*.joblib` already exist):

```bash
python -m src.train
```

This loads the dataset, trains all 4 candidate models, prints a comparison to the console, and saves the best model, vectorizer, metrics, and figures.

**Step 2 — Run the web app:**

```bash
python run.py
```

Then open **http://127.0.0.1:5000** in your browser.

**Step 3 — Try it out:**
- Paste a real headline/article, or click "Load Sample" for a quick demo.
- Visit `/about` to see full model statistics and charts.

## Web Application

Built with Flask using the application-factory pattern (`app/__init__.py`):

| Route | Method | Description |
|---|---|---|
| `/` | GET | Detector UI — submit a headline/article for classification |
| `/about` | GET | Model comparison table, dataset stats, evaluation charts |
| `/api/predict` | POST | JSON prediction API (used by the frontend via `fetch`) |
| `/reports/figures/<file>` | GET | Serves generated evaluation charts |

The frontend is vanilla HTML/CSS/JS (no build step required) — the prediction form submits via `fetch()` to `/api/predict` and animates a confidence bar based on the response.

## API Reference

**POST** `/api/predict`

Request body:
```json
{ "title": "Senate passes new infrastructure bill", "text": "Full article text here..." }
```

Response:
```json
{ "label": "REAL", "confidence": 87.42, "cleaned_word_count": 112 }
```

At least one of `title` or `text` must be non-empty. Errors return `400` (bad input) or `503` (model not yet trained).

## Testing

Unit tests cover text preprocessing and the inference layer:

```bash
pytest -v
```

## Limitations & Disclaimer

- The model learns **statistical writing-style patterns** from its training data — it does not fact-check claims against real-world knowledge or live sources.
- Performance reflects the training distribution (English-language news articles circa the dataset's collection period) and may not generalize to satire, non-English text, or novel misinformation styles.
- This tool is intended for **educational and research purposes**. Do not use it as a sole source of truth for high-stakes decisions.

## Future Improvements

- Add transformer-based models (e.g., DistilBERT) for comparison against classical baselines.
- Support batch/CSV upload for bulk article classification.
- Add explainability (e.g., LIME/SHAP) directly in the UI to highlight influential words per prediction.
- Containerize with Docker for one-command deployment.

## Tech Stack

- **ML/Data:** Python, scikit-learn, pandas, NumPy, joblib
- **Visualization:** Matplotlib
- **Backend:** Flask
- **Frontend:** HTML5, CSS3, vanilla JavaScript
- **Testing:** pytest

## License

This project is provided under the MIT License — see [LICENSE](LICENSE) for details. The bundled dataset retains its original source licensing/attribution.
"# Fake-News-Detection-Project" 
"# Fake-News-Detection-Project" 
