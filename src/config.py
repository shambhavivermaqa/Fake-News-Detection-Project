"""Central path and hyperparameter configuration for the project."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = ROOT_DIR / "dataset" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "dataset" / "processed"
MODELS_DIR = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RAW_DATASET_PATH = DATA_RAW_DIR / "fake_or_real_news.csv"
TRAIN_SPLIT_PATH = DATA_PROCESSED_DIR / "train.csv"
TEST_SPLIT_PATH = DATA_PROCESSED_DIR / "test.csv"

VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH = MODELS_DIR / "fake_news_model.joblib"
METRICS_PATH = REPORTS_DIR / "metrics.json"

RANDOM_STATE = 42
TEST_SIZE = 0.2

TFIDF_MAX_FEATURES = 50_000
TFIDF_NGRAM_RANGE = (1, 2)

LABELS = ["FAKE", "REAL"]
