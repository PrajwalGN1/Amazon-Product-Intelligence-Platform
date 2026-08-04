"""Data quality rules, schema checks, and executive scorecards."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.preprocessing import EXPECTED_COLUMNS


@dataclass(frozen=True)
class QualityRuleResult:
    """Result for one data quality rule."""

    rule: str
    failed_records: int
    severity: str
    business_impact: str


def validate_schema(df: pd.DataFrame) -> dict[str, object]:
    """Validate expected columns and detect schema drift."""

    actual = list(df.columns)
    missing = [column for column in EXPECTED_COLUMNS if column not in actual]
    unexpected = [column for column in actual if column not in EXPECTED_COLUMNS]
    return {
        "expected_columns": EXPECTED_COLUMNS,
        "actual_columns": actual,
        "missing_columns": missing,
        "unexpected_columns": unexpected,
        "schema_valid": not missing,
    }


def run_quality_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Run product data quality rules and return a scorecard table."""

    rules = [
        QualityRuleResult(
            "Missing product identifiers",
            int(df["product_id"].isna().sum()),
            "critical",
            "Breaks product-level joins and model inference.",
        ),
        QualityRuleResult(
            "Duplicate product identifiers",
            int(df["product_id"].duplicated().sum()),
            "high",
            "Can double-count product performance and distort ranking.",
        ),
        QualityRuleResult(
            "Invalid ratings outside 1-5",
            int((~df["rating_value"].between(1, 5)).sum()),
            "high",
            "Undermines customer satisfaction analysis.",
        ),
        QualityRuleResult(
            "Negative or zero discounted prices",
            int((df["discounted_price_value"] <= 0).sum()),
            "critical",
            "Creates unusable price and value recommendations.",
        ),
        QualityRuleResult(
            "Discount above 95 percent",
            int((df["discount_rate"] > 0.95).sum()),
            "medium",
            "May indicate extreme promotion or malformed price fields.",
        ),
        QualityRuleResult(
            "Missing review counts",
            int(df["review_count_missing"].sum()),
            "medium",
            "Reduces confidence in popularity and demand proxies.",
        ),
        QualityRuleResult(
            "Missing category",
            int(df["primary_category"].eq("Unknown").sum()),
            "high",
            "Prevents category performance attribution.",
        ),
    ]
    return pd.DataFrame([rule.__dict__ for rule in rules])


def calculate_quality_score(scorecard: pd.DataFrame, total_rows: int) -> float:
    """Calculate a weighted data quality score from rule failures."""

    weights = {"critical": 4.0, "high": 2.0, "medium": 1.0, "low": 0.5}
    penalty = sum(
        min(row.failed_records / max(total_rows, 1), 1) * weights[row.severity]
        for row in scorecard.itertuples(index=False)
    )
    max_penalty = sum(weights[row.severity] for row in scorecard.itertuples(index=False))
    return round(max(0.0, 100 * (1 - penalty / max_penalty)), 2)

