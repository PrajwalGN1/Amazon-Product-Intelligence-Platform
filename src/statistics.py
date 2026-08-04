"""Statistical analysis translated into business language."""

from __future__ import annotations

import pandas as pd
from scipy import stats


def discount_rating_hypothesis(df: pd.DataFrame) -> pd.DataFrame:
    """Test whether high-discount products have different ratings."""

    high_discount = df.loc[df["discount_rate"] >= df["discount_rate"].median(), "rating_value"]
    low_discount = df.loc[df["discount_rate"] < df["discount_rate"].median(), "rating_value"]
    result = stats.mannwhitneyu(high_discount, low_discount, alternative="two-sided")
    effect = high_discount.median() - low_discount.median()
    return pd.DataFrame(
        [
            {
                "hypothesis": "High-discount and low-discount products have different ratings",
                "test": "Mann-Whitney U",
                "p_value": round(float(result.pvalue), 6),
                "median_rating_difference": round(float(effect), 3),
                "business_interpretation": _interpret_p_value(result.pvalue, effect),
            }
        ]
    )


def numeric_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Return correlations among decision variables."""

    columns = [
        "discounted_price_value",
        "actual_price_value",
        "discount_rate",
        "rating_value",
        "rating_count_value",
        "business_priority_score",
    ]
    corr = df[columns].corr(numeric_only=True).reset_index(names="metric")
    return corr


def _interpret_p_value(p_value: float, effect: float) -> str:
    if p_value < 0.05 and effect > 0:
        return "Higher discounts are associated with higher customer ratings."
    if p_value < 0.05 and effect < 0:
        return "Higher discounts are associated with lower customer ratings."
    return "No statistically reliable rating difference by discount group."

