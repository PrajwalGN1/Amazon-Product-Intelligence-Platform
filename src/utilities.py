"""Shared utilities for logging and artifact persistence."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd


def get_logger(name: str) -> logging.Logger:
    """Return a configured project logger."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)


def ensure_directories(*paths: Path) -> None:
    """Create directories if they do not exist."""

    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    """Save a dataframe with a stable UTF-8 encoding."""

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")


def save_json(payload: dict[str, Any], path: Path) -> None:
    """Save a JSON artifact with readable formatting."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def dataframe_preview(df: pd.DataFrame, rows: int = 5) -> list[dict[str, Any]]:
    """Return a JSON-safe preview for reports."""

    return df.head(rows).replace({pd.NA: None}).to_dict(orient="records")

