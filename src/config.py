"""Project configuration and path helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Centralized filesystem configuration for reproducible runs."""

    project_root: Path = Path(__file__).resolve().parents[1]
    raw_data_path: Path = project_root / "data" / "raw" / "amazon.csv"
    processed_dir: Path = project_root / "data" / "processed"
    validation_dir: Path = project_root / "data" / "validation"
    reports_dir: Path = project_root / "reports"
    images_dir: Path = project_root / "images"
    models_dir: Path = project_root / "models"
    random_state: int = 42


CONFIG = ProjectConfig()

