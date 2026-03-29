from __future__ import annotations

from pathlib import Path

import pandas as pd

from logger import get_logger
from src.config_utils import load_config, resolve_project_path


try:
    import evaluate
    from transformers import pipeline
except ImportError as exc:
    raise RuntimeError(
        "Optional evaluation dependencies are missing. "
        "Install them with: pip install -r requirements-eval.txt"
    ) from exc


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
LOGGER = get_logger(__name__)


def load_dataset(dataset_path: Path) -> pd.DataFrame:
    """Load either CSV or Excel data and keep the article/summary columns only."""
    if dataset_path.suffix.lower() == ".xlsx":
        dataframe = pd.read_excel(dataset_path)
    else:
        dataframe = pd.read_csv(dataset_path)

    required_columns = {"article", "summary"}
    missing_columns = required_columns.difference(dataframe.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset at {dataset_path} is missing columns: {sorted(missing_columns)}"
        )

    return dataframe.loc[:, ["article", "summary"]].dropna().reset_index(drop=True)


def sample_rows(dataframe: pd.DataFrame, sample_size: int) -> pd.DataFrame:
    """Take a small deterministic sample to keep evaluation lightweight."""
    rows_to_use = min(sample_size, len(dataframe))
    if rows_to_use == len(dataframe):
        return dataframe.copy()
    return dataframe.sample(n=rows_to_use, random_state=42).reset_index(drop=True)


def truncate_article(article: str, max_words: int = 400) -> str:
    """Clip long articles so generation stays fast and memory-friendly."""
    words = str(article).split()
    return " ".join(words[:max_words])


def generate_summaries(
    summarizer,
    articles: list[str],
    batch_size: int,
    max_length: int = 60,
    min_length: int = 15,
) -> list[str]:
    """Generate summaries in small batches to avoid high memory use."""
    predictions: list[str] = []

    for batch_start in range(0, len(articles), batch_size):
        batch = articles[batch_start : batch_start + batch_size]
        outputs = summarizer(
            batch,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True,
            batch_size=batch_size,
        )
        predictions.extend(output["summary_text"] for output in outputs)

    return predictions


def evaluate_dataset(
    dataframe: pd.DataFrame,
    dataset_name: str,
    rouge,
    summarizer,
    model_name: str,
    batch_size: int,
) -> dict[str, float | int | str]:
    """Run summarization + ROUGE on a sampled dataset."""
    LOGGER.info("Starting baseline evaluation for %s dataset.", dataset_name)

    articles = [truncate_article(article) for article in dataframe["article"].tolist()]
    references = dataframe["summary"].astype(str).tolist()
    predictions = generate_summaries(summarizer, articles, batch_size=batch_size)

    scores = rouge.compute(
        predictions=predictions,
        references=references,
        use_stemmer=True,
    )

    result = {
        "dataset": dataset_name,
        "rows_used": len(dataframe),
        "model": model_name,
        "rouge1": round(scores["rouge1"], 4),
        "rouge2": round(scores["rouge2"], 4),
        "rougeL": round(scores["rougeL"], 4),
    }
    LOGGER.info("Finished baseline evaluation for %s dataset.", dataset_name)
    return result


def main() -> None:
    config = load_config(CONFIG_PATH)
    paths = config["paths"]
    parameters = config["parameters"]

    raw_data_path = resolve_project_path(PROJECT_ROOT, paths["raw_data"])
    processed_data_path = resolve_project_path(PROJECT_ROOT, paths["processed_data"])
    results_dir = resolve_project_path(PROJECT_ROOT, paths["results_output"])
    results_dir.mkdir(parents=True, exist_ok=True)

    sample_size = int(parameters.get("evaluation_sample_size", 50))
    batch_size = int(parameters.get("evaluation_batch_size", 2))
    model_name = str(parameters.get("baseline_model", "sshleifer/distilbart-cnn-12-6"))

    raw_df = sample_rows(load_dataset(raw_data_path), sample_size=sample_size)
    processed_df = sample_rows(load_dataset(processed_data_path), sample_size=sample_size)
    rouge = evaluate.load("rouge")
    summarizer = pipeline("summarization", model=model_name, tokenizer=model_name, device=-1)

    comparison_rows = [
        evaluate_dataset(
            raw_df,
            "raw",
            rouge=rouge,
            summarizer=summarizer,
            model_name=model_name,
            batch_size=batch_size,
        ),
        evaluate_dataset(
            processed_df,
            "newssumm_plus_plus",
            rouge=rouge,
            summarizer=summarizer,
            model_name=model_name,
            batch_size=batch_size,
        ),
    ]

    comparison_df = pd.DataFrame(comparison_rows)
    comparison_path = results_dir / "rouge_comparison.csv"
    comparison_df.to_csv(comparison_path, index=False)
    LOGGER.info("Saved ROUGE comparison to %s", comparison_path)


if __name__ == "__main__":
    main()
