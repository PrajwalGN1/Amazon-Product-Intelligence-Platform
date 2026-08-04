"""Business feature engineering for decision intelligence."""

from __future__ import annotations

import numpy as np
import pandas as pd


def minmax(series: pd.Series) -> pd.Series:
    """Scale a numeric series into the 0-1 range."""

    values = pd.to_numeric(series, errors="coerce").fillna(0)
    span = values.max() - values.min()
    if span == 0:
        return pd.Series(np.zeros(len(values)), index=values.index)
    return (values - values.min()) / span


def add_business_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create decision-ready product, price, trust, and opportunity features."""

    featured = df.copy()
    featured["weighted_rating"] = (
        featured["rating_value"] * np.log1p(featured["rating_count_value"])
    )
    category_review_avg = featured.groupby("primary_category")[
        "rating_count_value"
    ].transform("mean")
    category_price_avg = featured.groupby("primary_category")[
        "discounted_price_value"
    ].transform("mean")
    global_mean = featured["rating_value"].mean()
    confidence = featured["rating_count_value"] / (
        featured["rating_count_value"] + 250
    )
    featured["bayesian_rating"] = (
        confidence * featured["rating_value"] + (1 - confidence) * global_mean
    )
    featured["popularity_index"] = minmax(np.log1p(featured["rating_count_value"]))
    featured["value_score"] = minmax(
        featured["rating_value"] / featured["discounted_price_value"].clip(lower=1)
    )
    featured["price_competitiveness_index"] = minmax(
        category_price_avg / featured["discounted_price_value"].clip(lower=1)
    )
    featured["customer_trust_index"] = minmax(
        featured["bayesian_rating"] * np.log1p(featured["rating_count_value"])
    )
    featured["discount_effectiveness_score"] = minmax(
        featured["discount_rate"] * featured["rating_value"]
    )
    featured["review_engagement_ratio"] = (
        featured["rating_count_value"] / category_review_avg.replace(0, np.nan)
    ).fillna(0)
    featured["revenue_opportunity_score"] = minmax(
        featured["price_gap"] * np.log1p(featured["rating_count_value"])
    )
    featured["sentiment_proxy_score"] = minmax(
        featured["rating_value"] + featured["review_text_length"] / 1000
    )
    featured["business_priority_score"] = (
        0.25 * featured["customer_trust_index"]
        + 0.25 * featured["popularity_index"]
        + 0.20 * featured["revenue_opportunity_score"]
        + 0.15 * featured["price_competitiveness_index"]
        + 0.15 * featured["discount_effectiveness_score"]
    )
    featured["price_tier"] = pd.qcut(
        featured["discounted_price_value"].rank(method="first"),
        q=4,
        labels=["Budget", "Value", "Premium", "Luxury"],
    )
    featured["success_label"] = (
        featured["business_priority_score"]
        >= featured["business_priority_score"].quantile(0.75)
    ).astype(int)
    return featured

