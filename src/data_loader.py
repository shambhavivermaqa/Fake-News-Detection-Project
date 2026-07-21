"""Loads the raw dataset, cleans it, and produces a reproducible train/test split."""

import pandas as pd
from sklearn.model_selection import train_test_split

from src import config
from src.preprocess import build_input_text


def load_raw_dataset() -> pd.DataFrame:
    if not config.RAW_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {config.RAW_DATASET_PATH}. "
            "See README.md 'Dataset' section for download instructions."
        )
    df = pd.read_csv(config.RAW_DATASET_PATH)
    df = df.dropna(subset=["title", "text", "label"]).drop_duplicates(subset=["title", "text"])
    df["label"] = df["label"].str.upper().str.strip()
    df = df[df["label"].isin(config.LABELS)].reset_index(drop=True)
    df["clean_text"] = [
        build_input_text(t, b) for t, b in zip(df["title"], df["text"])
    ]
    df = df[df["clean_text"].str.len() > 0].reset_index(drop=True)
    return df


def make_splits(df: pd.DataFrame):
    train_df, test_df = train_test_split(
        df,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=df["label"],
    )
    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def load_or_create_splits():
    """Return (train_df, test_df), persisting them to dataset/processed on first run."""
    if config.TRAIN_SPLIT_PATH.exists() and config.TEST_SPLIT_PATH.exists():
        return (
            pd.read_csv(config.TRAIN_SPLIT_PATH),
            pd.read_csv(config.TEST_SPLIT_PATH),
        )

    df = load_raw_dataset()
    train_df, test_df = make_splits(df)
    config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(config.TRAIN_SPLIT_PATH, index=False)
    test_df.to_csv(config.TEST_SPLIT_PATH, index=False)
    return train_df, test_df
