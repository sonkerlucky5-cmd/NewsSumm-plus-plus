from __future__ import annotations

import unittest
from pathlib import Path

import pandas as pd
import spacy
from spacy.pipeline import EntityRuler

from logger import get_logger
from src.cleaning import basic_clean_text, clean_dataset
from src.config_utils import load_config
from src.entity_extraction import add_entity_counts
from src.feature_engineering import add_length_features, safe_readability, safe_word_count
from src.metrics import (
    create_dataset_stats_table,
    create_error_analysis_table,
    create_main_results_table,
)


class CleaningTests(unittest.TestCase):
    def test_basic_clean_text_removes_extra_spaces_and_urls(self) -> None:
        text = " Hello   world \n visit https://example.com now "
        cleaned = basic_clean_text(text)
        self.assertEqual(cleaned, "Hello world visit now")

    def test_clean_dataset_removes_duplicates_and_short_rows(self) -> None:
        df = pd.DataFrame(
            {
                "article": [
                    "word " * 35,
                    "word " * 35,
                    "tiny text",
                ],
                "summary": [
                    "summary " * 6,
                    "summary " * 6,
                    "short",
                ],
            }
        )

        cleaned = clean_dataset(df)
        self.assertEqual(len(cleaned), 1)


class FeatureEngineeringTests(unittest.TestCase):
    def test_word_count_and_readability_are_numeric(self) -> None:
        self.assertEqual(safe_word_count("one two three"), 3)
        self.assertIsInstance(safe_readability("This is a short and readable sentence."), float)

    def test_add_length_features_adds_expected_columns(self) -> None:
        df = pd.DataFrame(
            {
                "article": ["This is a simple article with enough words to measure correctly."],
                "summary": ["This summary is short but valid."],
            }
        )

        enriched = add_length_features(df)
        expected_columns = {
            "doc_length",
            "summary_length",
            "compression_ratio",
            "readability_score",
        }
        self.assertTrue(expected_columns.issubset(set(enriched.columns)))


class EntityExtractionTests(unittest.TestCase):
    def test_add_entity_counts_works_with_custom_pipeline(self) -> None:
        nlp = spacy.blank("en")
        ruler = nlp.add_pipe("entity_ruler")
        assert isinstance(ruler, EntityRuler)
        ruler.add_patterns(
            [
                {"label": "GPE", "pattern": "Austin"},
                {"label": "ORG", "pattern": "North Valley Hospital"},
            ]
        )

        df = pd.DataFrame(
            {
                "article": ["Austin officials met leaders from North Valley Hospital yesterday."],
                "summary": ["Austin officials met hospital leaders."],
            }
        )
        df = add_length_features(df)
        enriched = add_entity_counts(df, nlp=nlp)

        self.assertIn("entity_count", enriched.columns)
        self.assertGreaterEqual(int(enriched.loc[0, "entity_count"]), 2)


class MetricsTests(unittest.TestCase):
    def test_metrics_tables_have_expected_shape(self) -> None:
        df = pd.DataFrame(
            {
                "article": [
                    "Austin launched a program for residents needing faster city service support."
                ],
                "summary": ["Austin launched a city support program."],
            }
        )
        df = add_length_features(df)
        df["entity_count"] = [2]

        dataset_stats = create_dataset_stats_table(df)
        main_results = create_main_results_table(df)
        error_analysis = create_error_analysis_table(df)

        self.assertEqual(list(dataset_stats.columns), ["metric", "value"])
        self.assertIn("model", main_results.columns)
        self.assertEqual(list(error_analysis.columns), ["issue", "count"])


class ConfigAndLoggerTests(unittest.TestCase):
    def test_config_file_loads_expected_sections(self) -> None:
        config = load_config(Path("config.yaml"))
        self.assertIn("paths", config)
        self.assertIn("parameters", config)
        self.assertIn("raw_data", config["paths"])
        self.assertIn("spacy_model", config["parameters"])

    def test_logger_returns_named_logger(self) -> None:
        logger = get_logger("test_logger")
        self.assertEqual(logger.name, "test_logger")


if __name__ == "__main__":
    unittest.main()
