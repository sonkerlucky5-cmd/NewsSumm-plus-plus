from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from logger import get_logger
from src.feature_engineering import safe_readability


LOGGER = get_logger(__name__)


def plot_document_length_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.hist(
        df["doc_length"],
        bins=min(max(len(df), 5), 12),
        color="#2E6F95",
        edgecolor="white",
    )
    plt.title("Document Length Distribution")
    plt.xlabel("Document Length (words)")
    plt.ylabel("Number of Articles")
    plt.tight_layout()
    plt.savefig(output_dir / "document_length_distribution.png", dpi=200)
    plt.close()
    LOGGER.info("Saved document length distribution graph.")


def plot_readability_comparison(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    average_article_readability = round(df["readability_score"].mean(), 2)
    average_summary_readability = round(df["summary"].apply(safe_readability).mean(), 2)

    plt.figure(figsize=(7, 5))
    plt.bar(
        ["Articles", "Summaries"],
        [average_article_readability, average_summary_readability],
        color=["#2E6F95", "#FFB703"],
    )
    plt.title("Average Readability Comparison")
    plt.ylabel("Automated Readability Index")
    plt.tight_layout()
    plt.savefig(output_dir / "readability_comparison.png", dpi=200)
    plt.close()
    LOGGER.info("Saved readability comparison graph.")


def generate_graphs(df: pd.DataFrame, output_dir: Path) -> None:
    plot_document_length_distribution(df, output_dir)
    plot_readability_comparison(df, output_dir)
