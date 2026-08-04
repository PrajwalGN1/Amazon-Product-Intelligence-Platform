"""Reusable visualization functions for reports and notebooks."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def set_visual_style() -> None:
    """Apply a clean executive reporting style."""

    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["figure.figsize"] = (12, 7)
    plt.rcParams["axes.titleweight"] = "bold"


def save_category_priority_chart(category_df: pd.DataFrame, path: Path) -> None:
    """Save a bar chart of category priority scores."""

    set_visual_style()
    top = category_df.head(10).sort_values("priority_score")
    fig, ax = plt.subplots()
    sns.barplot(data=top, x="priority_score", y="primary_category", ax=ax, color="#2A9D8F")
    ax.set_title("Category Priority Score")
    ax.set_xlabel("Average business priority score")
    ax.set_ylabel("")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def save_price_rating_chart(df: pd.DataFrame, path: Path) -> None:
    """Save a price versus rating chart colored by discount."""

    set_visual_style()
    sample = df.sort_values("rating_count_value", ascending=False).head(600)
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=sample,
        x="discounted_price_value",
        y="rating_value",
        hue="discount_rate",
        size="rating_count_value",
        sizes=(20, 300),
        alpha=0.65,
        ax=ax,
        palette="viridis",
    )
    ax.set_xscale("log")
    ax.set_title("Price, Rating and Discount Relationship")
    ax.set_xlabel("Discounted price, log scale")
    ax.set_ylabel("Customer rating")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)

