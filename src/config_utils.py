from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: Path) -> dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Config file must contain a top-level mapping.")

    return config


def resolve_project_path(project_root: Path, relative_path: str) -> Path:
    return project_root / Path(relative_path)
