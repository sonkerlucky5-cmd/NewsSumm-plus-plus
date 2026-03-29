from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from logger import get_logger


REQUIRED_COLUMNS = {"article", "summary"}
LOGGER = get_logger(__name__)


def load_raw_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)
    LOGGER.info("Loaded %s raw rows from %s", len(df), csv_path)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset must contain columns {sorted(REQUIRED_COLUMNS)}. "
            f"Missing: {sorted(missing_columns)}"
        )
    return df.loc[:, ["article", "summary"]]


def basic_clean_text(text: object) -> str:
    if pd.isna(text):
        return ""

    cleaned = str(text)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)
    cleaned = cleaned.replace("\n", " ").replace("\t", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([,.!?;:])", r"\1", cleaned)
    return cleaned.strip()


def clean_dataset(
    df: pd.DataFrame,
    min_article_words: int = 30,
    min_summary_words: int = 5,
) -> pd.DataFrame:
    original_rows = len(df)
    cleaned_df = df.copy()
    cleaned_df["article"] = cleaned_df["article"].apply(basic_clean_text)
    cleaned_df["summary"] = cleaned_df["summary"].apply(basic_clean_text)
    cleaned_df = cleaned_df.dropna(subset=["article", "summary"])
    cleaned_df = cleaned_df[
        (cleaned_df["article"] != "") & (cleaned_df["summary"] != "")
    ]
    cleaned_df = cleaned_df.drop_duplicates(subset=["article", "summary"])

    article_lengths = cleaned_df["article"].str.split().str.len()
    summary_lengths = cleaned_df["summary"].str.split().str.len()
    cleaned_df = cleaned_df[
        (article_lengths >= min_article_words) & (summary_lengths >= min_summary_words)
    ].copy()

    LOGGER.info(
        "Cleaning complete: %s -> %s rows after removing duplicates, blanks, and short rows.",
        original_rows,
        len(cleaned_df),
    )
    return cleaned_df.reset_index(drop=True)
