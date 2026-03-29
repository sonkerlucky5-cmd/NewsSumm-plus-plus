from __future__ import annotations

import math

import pandas as pd
from textstat import textstat

from logger import get_logger


LOGGER = get_logger(__name__)


def safe_word_count(text: str) -> int:
    if not text:
        return 0
    return len(text.split())


def safe_readability(text: str) -> float:
    if not text:
        return 0.0

    score = textstat.automated_readability_index(text)
    if score is None or (isinstance(score, float) and math.isnan(score)):
        return 0.0
    return round(float(score), 2)


def add_length_features(df: pd.DataFrame) -> pd.DataFrame:
    featured_df = df.copy()
    featured_df["doc_length"] = featured_df["article"].apply(safe_word_count)
    featured_df["summary_length"] = featured_df["summary"].apply(safe_word_count)
    featured_df["compression_ratio"] = (
        featured_df["summary_length"] / featured_df["doc_length"].replace(0, pd.NA)
    ).fillna(0.0)
    featured_df["compression_ratio"] = featured_df["compression_ratio"].round(4)
    featured_df["readability_score"] = featured_df["article"].apply(safe_readability)
    LOGGER.info("Added length and readability features to %s rows.", len(featured_df))
    return featured_df
