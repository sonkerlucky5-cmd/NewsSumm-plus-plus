from __future__ import annotations

import pandas as pd
import spacy
from spacy.language import Language

from logger import get_logger


MODEL_NAME = "en_core_web_sm"
LOGGER = get_logger(__name__)


def load_spacy_model(model_name: str = MODEL_NAME) -> Language:
    try:
        nlp = spacy.load(model_name, disable=["parser", "textcat"])
        LOGGER.info("spaCy model '%s' loaded successfully.", model_name)
        return nlp
    except OSError as exc:
        raise RuntimeError(
            f"spaCy model '{model_name}' is not installed. Run the setup script first."
        ) from exc


def add_entity_counts(
    df: pd.DataFrame,
    nlp: Language | None = None,
    batch_size: int = 32,
) -> pd.DataFrame:
    entity_df = df.copy()
    nlp = nlp or load_spacy_model()

    entity_counts = []
    for doc in nlp.pipe(entity_df["article"].fillna("").tolist(), batch_size=batch_size):
        entity_counts.append(len(doc.ents))

    entity_df["entity_count"] = entity_counts
    LOGGER.info("Calculated named entity counts for %s rows.", len(entity_df))
    return entity_df
