"""Shared utility helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import pandas as pd


def setup_logging() -> None:
    """Configure consistent console logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def ensure_directories(paths: Iterable[Path]) -> None:
    """Create project directories when missing."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def first_existing_column(df: pd.DataFrame, candidates: Iterable[str]) -> str | None:
    """Return the first matching column from a list of common dataset variants."""
    lower_to_original = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_to_original:
            return lower_to_original[candidate.lower()]
    return None


def safe_read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV with a practical fallback for noisy social data exports."""
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

