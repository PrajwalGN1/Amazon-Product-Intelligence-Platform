"""Data loading and cleaning for Amazon product catalog data."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

EXPECTED_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
    "about_product",
    "user_id",
    "user_name",
    "review_id",
    "review_title",
    "review_content",
    "img_link",
    "product_link",
]


def load_raw_data(path: Path) -> pd.DataFrame:
    """Load the raw Amazon CSV and preserve the source columns."""

    return pd.read_csv(path)


def parse_currency(value: object) -> float:
    """Convert rupee-formatted currency strings into numeric values."""

    if pd.isna(value):
        return np.nan
    normalized = str(value).replace(",", "")
    matches = re.findall(r"\d+(?:\.\d+)?", normalized)
    return float(matches[0]) if matches else np.nan


def parse_percentage(value: object) -> float:
    """Convert percentage strings like '64%' into a decimal share."""

    if pd.isna(value):
        return np.nan
    cleaned = re.sub(r"[^0-9.]", "", str(value))
    return float(cleaned) / 100 if cleaned else np.nan


def parse_count(value: object) -> float:
    """Convert comma-formatted review counts into numeric values."""

    if pd.isna(value):
        return np.nan
    cleaned = re.sub(r"[^0-9]", "", str(value))
    return float(cleaned) if cleaned else np.nan


def split_category(category: object) -> list[str]:
    """Split the Amazon category hierarchy into clean tokens."""

    if pd.isna(category):
        return []
    return [part.strip() for part in str(category).split("|") if part.strip()]


def clean_product_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw records and create typed analysis columns."""

    cleaned = df.copy()
    cleaned.columns = [column.strip() for column in cleaned.columns]
    cleaned["discounted_price_value"] = cleaned["discounted_price"].map(parse_currency)
    cleaned["actual_price_value"] = cleaned["actual_price"].map(parse_currency)
    cleaned["discount_rate"] = cleaned["discount_percentage"].map(parse_percentage)
    cleaned["rating_value"] = pd.to_numeric(cleaned["rating"], errors="coerce")
    cleaned["rating_count_value"] = cleaned["rating_count"].map(parse_count)
    cleaned["category_path"] = cleaned["category"].map(split_category)
    cleaned["primary_category"] = cleaned["category_path"].map(
        lambda parts: parts[0] if parts else "Unknown"
    )
    cleaned["secondary_category"] = cleaned["category_path"].map(
        lambda parts: parts[1] if len(parts) > 1 else "Unknown"
    )
    cleaned["product_name_length"] = cleaned["product_name"].astype(str).str.len()
    cleaned["about_product_length"] = cleaned["about_product"].astype(str).str.len()
    cleaned["review_text_length"] = cleaned["review_content"].astype(str).str.len()
    cleaned["review_count_missing"] = cleaned["rating_count_value"].isna()
    cleaned["rating_count_value"] = cleaned["rating_count_value"].fillna(0)
    cleaned["price_gap"] = (
        cleaned["actual_price_value"] - cleaned["discounted_price_value"]
    )
    cleaned["price_gap"] = cleaned["price_gap"].clip(lower=0)
    return cleaned
