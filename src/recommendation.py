"""Content-based recommendation engine for Amazon products."""

from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_product_text(df: pd.DataFrame) -> pd.Series:
    """Combine product fields into one recommendation corpus."""

    return (
        df["product_name"].fillna("")
        + " "
        + df["category"].fillna("")
        + " "
        + df["about_product"].fillna("")
        + " "
        + df["review_title"].fillna("")
    )


def recommend_similar_products(
    df: pd.DataFrame, product_id: str, top_n: int = 10
) -> pd.DataFrame:
    """Recommend similar products using TF-IDF cosine similarity."""

    if product_id not in set(df["product_id"]):
        raise ValueError(f"Product id not found: {product_id}")
    corpus = build_product_text(df)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    matrix = vectorizer.fit_transform(corpus)
    index = df.index[df["product_id"].eq(product_id)][0]
    scores = cosine_similarity(matrix[index], matrix).ravel()
    candidates = df.copy()
    candidates["similarity_score"] = scores
    candidates = candidates[candidates["product_id"] != product_id]
    columns = [
        "product_id",
        "product_name",
        "primary_category",
        "rating_value",
        "rating_count_value",
        "similarity_score",
    ]
    return candidates.sort_values("similarity_score", ascending=False)[columns].head(top_n)

