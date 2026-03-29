from __future__ import annotations

from pathlib import Path

import pandas as pd
from rouge_score import rouge_scorer

from logger import get_logger


LOGGER = get_logger(__name__)


def create_dataset_stats_table(df: pd.DataFrame) -> pd.DataFrame:
    stats = [
        ("row_count", len(df)),
        ("avg_doc_length", round(df["doc_length"].mean(), 2)),
        ("avg_summary_length", round(df["summary_length"].mean(), 2)),
        ("avg_compression_ratio", round(df["compression_ratio"].mean(), 4)),
        ("avg_readability_score", round(df["readability_score"].mean(), 2)),
        ("avg_entity_count", round(df["entity_count"].mean(), 2)),
    ]
    return pd.DataFrame(stats, columns=["metric", "value"])


def _build_lead_baseline(article: str, target_length: int) -> str:
    words = article.split()
    if not words:
        return ""
    clipped_length = max(1, min(target_length, len(words)))
    return " ".join(words[:clipped_length])


def create_main_results_table(df: pd.DataFrame) -> pd.DataFrame:
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge_totals = {"rouge1_f1": [], "rouge2_f1": [], "rougeL_f1": []}

    for row in df.itertuples(index=False):
        prediction = _build_lead_baseline(row.article, row.summary_length)
        scores = scorer.score(row.summary, prediction)
        rouge_totals["rouge1_f1"].append(scores["rouge1"].fmeasure)
        rouge_totals["rouge2_f1"].append(scores["rouge2"].fmeasure)
        rouge_totals["rougeL_f1"].append(scores["rougeL"].fmeasure)

    return pd.DataFrame(
        [
            {
                "model": "Lead-word baseline",
                "rouge1_f1": round(sum(rouge_totals["rouge1_f1"]) / len(df), 4),
                "rouge2_f1": round(sum(rouge_totals["rouge2_f1"]) / len(df), 4),
                "rougeL_f1": round(sum(rouge_totals["rougeL_f1"]) / len(df), 4),
                "notes": "Baseline uses the first N article words, where N matches summary length.",
            }
        ]
    )


def create_error_analysis_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("short_documents_under_60_words", int((df["doc_length"] < 60).sum())),
        ("long_documents_over_120_words", int((df["doc_length"] > 120).sum())),
        ("low_readability_below_50", int((df["readability_score"] < 50).sum())),
        ("high_compression_above_0.35", int((df["compression_ratio"] > 0.35).sum())),
        ("rows_with_no_entities", int((df["entity_count"] == 0).sum())),
    ]
    return pd.DataFrame(rows, columns=["issue", "count"])


def generate_analysis_tables(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_stats = create_dataset_stats_table(df)
    main_results = create_main_results_table(df)
    error_analysis = create_error_analysis_table(df)

    dataset_stats.to_excel(output_dir / "dataset_stats.xlsx", index=False)
    dataset_stats.to_csv(output_dir / "dataset_stats.csv", index=False)
    main_results.to_excel(output_dir / "main_results.xlsx", index=False)
    main_results.to_csv(output_dir / "main_results.csv", index=False)
    error_analysis.to_excel(output_dir / "error_analysis.xlsx", index=False)
    error_analysis.to_csv(output_dir / "error_analysis.csv", index=False)
    LOGGER.info("Saved analysis tables to %s", output_dir)
