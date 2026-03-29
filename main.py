import os
import tempfile
from pathlib import Path

from logger import get_logger
from src.config_utils import load_config, resolve_project_path


PROJECT_ROOT = Path(__file__).resolve().parent
os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "newssum_matplotlib"),
)

from src.cleaning import clean_dataset, load_raw_data
from src.entity_extraction import add_entity_counts, load_spacy_model
from src.feature_engineering import add_length_features
from src.metrics import generate_analysis_tables
from src.visualization import generate_graphs


LOGGER = get_logger(__name__)
CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def ensure_directories(*directories: Path) -> None:
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def run_pipeline() -> None:
    config = load_config(CONFIG_PATH)
    paths = config["paths"]
    parameters = config["parameters"]

    raw_data_path = resolve_project_path(PROJECT_ROOT, paths["raw_data"])
    processed_data_path = resolve_project_path(PROJECT_ROOT, paths["processed_data"])
    metrics_output_path = resolve_project_path(PROJECT_ROOT, paths["metrics_output"])
    graphs_output_path = resolve_project_path(PROJECT_ROOT, paths["graphs_output"])
    results_output_path = resolve_project_path(PROJECT_ROOT, paths["results_output"])

    ensure_directories(
        raw_data_path.parent,
        processed_data_path.parent,
        metrics_output_path,
        graphs_output_path,
        results_output_path,
    )

    min_doc_length = int(parameters.get("min_doc_length", 50))
    min_summary_length = int(parameters.get("min_summary_length", 5))
    spacy_model = str(parameters.get("spacy_model", "en_core_web_sm"))

    LOGGER.info("Loading raw data from %s", raw_data_path)
    raw_df = load_raw_data(raw_data_path)
    cleaned_df = clean_dataset(
        raw_df,
        min_article_words=min_doc_length,
        min_summary_words=min_summary_length,
    )
    if cleaned_df.empty:
        raise ValueError("No rows remain after cleaning. Check the raw dataset contents.")

    LOGGER.info("Adding feature engineering columns.")
    enriched_df = add_length_features(cleaned_df)
    LOGGER.info("Loading spaCy model: %s", spacy_model)
    nlp = load_spacy_model(spacy_model)
    final_df = add_entity_counts(enriched_df, nlp=nlp)

    final_df.to_excel(processed_data_path, index=False)
    generate_analysis_tables(final_df, metrics_output_path)
    generate_graphs(final_df, graphs_output_path)

    LOGGER.info("Pipeline completed successfully with %s rows.", len(final_df))
    LOGGER.info("Processed dataset: %s", processed_data_path)
    LOGGER.info("Tables directory: %s", metrics_output_path)
    LOGGER.info("Graphs directory: %s", graphs_output_path)


if __name__ == "__main__":
    run_pipeline()
