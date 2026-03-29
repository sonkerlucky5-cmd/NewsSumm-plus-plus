from __future__ import annotations

import logging
from pathlib import Path


LOGS_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOGS_DIR / "pipeline.log"
LOG_FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(filename)s] - [%(message)s]"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a project logger that writes to both console and file."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name or "newssumm")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


# Example usage in other files:
# from logger import get_logger
# logger = get_logger(__name__)
# logger.info("Cleaning pipeline started.")


if __name__ == "__main__":
    example_logger = get_logger(__name__)
    example_logger.info("Logger is configured and ready to use.")
