"""Executive business analytics and recommendation tables."""

from __future__ import annotations

import pandas as pd


def executive_kpis(df: pd.DataFrame) -> dict[str, float]:
    """Calculate top-level KPIs for executives."""

    return {
        "products": int(df["product_id"].nunique()),
        "categories": int(df["primary_category"].nunique()),
        "average_rating": round(float(df["rating_value"].mean()), 2),
        "average_discount": round(float(df["discount_rate"].mean()), 3),
        "median_discounted_price": round(float(df["discounted_price_value"].median()), 2),
        "total_review_proxy": int(df["rating_count_value"].sum()),
        "high_priority_products": int(df["success_label"].sum()),
    }


def category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize performance by primary category."""

    summary = (
        df.groupby("primary_category")
        .agg(
            products=("product_id", "nunique"),
            avg_rating=("rating_value", "mean"),
            avg_discount=("discount_rate", "mean"),
            median_price=("discounted_price_value", "median"),
            review_proxy=("rating_count_value", "sum"),
            priority_score=("business_priority_score", "mean"),
        )
        .reset_index()
    )
    summary["management_action"] = summary.apply(_category_action, axis=1)
    return summary.sort_values("priority_score", ascending=False)


def product_priority_table(df: pd.DataFrame, top_n: int = 25) -> pd.DataFrame:
    """Rank products for promotion, optimization, and advertising actions."""

    columns = [
        "product_id",
        "product_name",
        "primary_category",
        "discounted_price_value",
        "actual_price_value",
        "discount_rate",
        "rating_value",
        "rating_count_value",
        "business_priority_score",
        "customer_trust_index",
        "revenue_opportunity_score",
    ]
    ranked = df[columns].sort_values("business_priority_score", ascending=False).head(top_n)
    ranked = ranked.copy()
    ranked["recommended_action"] = ranked.apply(_product_action, axis=1)
    return ranked


def pricing_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    """Identify products where price and discount strategy need attention."""

    opportunities = df[
        [
            "product_id",
            "product_name",
            "primary_category",
            "discounted_price_value",
            "actual_price_value",
            "discount_rate",
            "rating_value",
            "price_competitiveness_index",
            "discount_effectiveness_score",
        ]
    ].copy()
    opportunities["pricing_signal"] = opportunities.apply(_pricing_signal, axis=1)
    return opportunities.sort_values(
        ["price_competitiveness_index", "rating_value"], ascending=[True, False]
    )


def _category_action(row: pd.Series) -> str:
    if row.avg_rating >= 4.2 and row.review_proxy > 100000:
        return "Scale promotions and protect availability."
    if row.avg_rating < 4.0:
        return "Investigate customer dissatisfaction before expanding spend."
    if row.avg_discount > 0.55:
        return "Audit margin impact from aggressive discounting."
    return "Maintain monitoring and test selective campaigns."


def _product_action(row: pd.Series) -> str:
    trust = float(row.customer_trust_index)
    revenue_opp = float(row.revenue_opportunity_score)
    discount = float(row.discount_rate)
    rating = float(row.rating_value)
    reviews = int(row.rating_count_value)
    priority = float(row.business_priority_score)
    price = float(row.discounted_price_value)
    
    if priority >= 0.65 and trust >= 0.90:
        return f"Scale ad spend; capitalize on {trust:.2f} trust index and {rating} rating."
    if rating >= 4.4 and discount > 0.55:
        return f"Taper {discount:.0%} discount to capture margin on highly rated (Rs.{price:,.0f}) item."
    if discount >= 0.60 and rating < 4.0:
        return f"Heavy discount ({discount:.0%}) isn't fixing {rating} rating; audit quality."
    if trust >= 0.75 and revenue_opp >= 0.15:
        return f"Promote aggressively to unlock {revenue_opp:.2f} revenue upside."
    if reviews > 150000 and rating >= 4.1:
        return f"Protect inventory for this high-volume staple ({reviews:,} reviews)."
    if reviews < 1000 and rating >= 4.0:
        return f"Increase visibility to build on {reviews} reviews and {rating} rating."
    if priority >= 0.60 and trust < 0.80:
        return f"Improve page content to boost {trust:.2f} trust score."
    if reviews > 50000 and discount < 0.20:
        return f"Test slight promotional discount to accelerate volume."
    
    return f"Monitor placement (Priority: {priority:.2f}, Rating: {rating})."


def _pricing_signal(row: pd.Series) -> str:
    if row.price_competitiveness_index < 0.25 and row.rating_value < 4.0:
        return "Likely overpriced relative to customer value."
    if row.discount_rate > 0.70 and row.rating_value >= 4.2:
        return "Discount is working, validate margin tolerance."
    if row.discount_rate > 0.70 and row.rating_value < 4.0:
        return "Discount is not repairing customer perception."
    return "No urgent price intervention."

