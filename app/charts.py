"""Plotly charts for the executive Streamlit frontend."""

from __future__ import annotations

import pandas as pd
# pyrefly: ignore [missing-import]
import plotly.express as px
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go

PALETTE = ["#FF9900", "#146EB4", "#2E7D32", "#F9A825", "#C62828", "#232F3E"]


def apply_enterprise_theme(fig: go.Figure, height: int = 420) -> go.Figure:
    """Apply common chart styling."""

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Inter, Arial", "color": "#1F2937"},
        title={
            "font": {"family": "Inter, Arial", "size": 20, "color": "#232F3E"},
            "x": 0.02,
            "xanchor": "left",
        },
        margin={"l": 20, "r": 20, "t": 70, "b": 30},
        legend={
            "orientation": "h",
            "y": -0.15,
            "font": {"family": "Inter, Arial", "size": 12, "color": "#1F2937"},
        },
        coloraxis_colorbar={
            "title": {"font": {"color": "#232F3E", "size": 13}},
            "tickfont": {"color": "#475467", "size": 12},
        },
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        color="#475467",
        title_font={"color": "#232F3E", "size": 14},
        tickfont={"color": "#475467", "size": 12},
        linecolor="#D0D5DD",
    )
    fig.update_yaxes(
        gridcolor="#EEF2F6",
        zeroline=False,
        color="#475467",
        title_font={"color": "#232F3E", "size": 14},
        tickfont={"color": "#475467", "size": 12},
        linecolor="#D0D5DD",
    )
    hover_label = {
    "bgcolor": "#FFFFFF",
    "font": {
        "family": "Inter, Arial",
        "color": "#1F2937",
    },
    "bordercolor": "#D0D5DD",
}

    for trace in fig.data:
        # Indicator traces do not support hoverlabel
        if isinstance(trace, go.Indicator):
            continue

        try:
            trace.update(hoverlabel=hover_label)
        except (ValueError, AttributeError):
            pass

    return fig


def category_treemap(category_df: pd.DataFrame) -> go.Figure:
    """Render category contribution as a treemap."""

    fig = px.treemap(
        category_df,
        path=["primary_category"],
        values="review_proxy",
        color="priority_score",
        color_continuous_scale=["#F6F7F9", "#FF9900", "#146EB4"],
        title="Category Demand and Priority Map",
    )
    fig.update_traces(textfont={"color": "#1F2937", "size": 14})
    return apply_enterprise_theme(fig, 460)


def category_sunburst(df: pd.DataFrame) -> go.Figure:
    """Render product hierarchy as a sunburst."""

    hierarchy = (
        df.groupby(["primary_category", "secondary_category"], dropna=False)
        .agg(review_proxy=("rating_count_value", "sum"), avg_rating=("rating_value", "mean"))
        .reset_index()
    )
    fig = px.sunburst(
        hierarchy,
        path=["primary_category", "secondary_category"],
        values="review_proxy",
        color="avg_rating",
        color_continuous_scale=["#C62828", "#F9A825", "#2E7D32"],
        title="Category Hierarchy and Customer Satisfaction",
    )
    fig.update_traces(insidetextfont={"color": "#1F2937"}, outsidetextfont={"color": "#1F2937"})
    return apply_enterprise_theme(fig, 460)


def price_rating_bubble(df: pd.DataFrame) -> go.Figure:
    """Render interactive price-rating-discount relationships."""

    plot_df = df.sort_values("rating_count_value", ascending=False).head(700)
    fig = px.scatter(
        plot_df,
        x="discounted_price_value",
        y="rating_value",
        size="rating_count_value",
        color="discount_rate",
        hover_name="product_name",
        hover_data=["primary_category", "business_priority_score"],
        log_x=True,
        color_continuous_scale=["#146EB4", "#FF9900", "#C62828"],
        title="Price, Rating, Discount and Demand Relationship",
    )
    return apply_enterprise_theme(fig, 500)


def performance_heatmap(df: pd.DataFrame) -> go.Figure:
    """Render category and price tier performance heatmap."""

    matrix = (
        df.pivot_table(
            index="primary_category",
            columns="price_tier",
            values="business_priority_score",
            aggfunc="mean",
        )
        .fillna(0)
        .round(3)
    )
    fig = px.imshow(
        matrix,
        color_continuous_scale=["#FFFFFF", "#FF9900", "#146EB4"],
        aspect="auto",
        title="Business Priority Heatmap by Category and Price Tier",
    )
    fig.update_traces(colorbar={"tickfont": {"color": "#475467"}})
    return apply_enterprise_theme(fig, 430)


def business_health_gauge(score: float) -> go.Figure:
    """Render a gauge for catalog health."""

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "/100", "font": {"size": 42, "color": "#232F3E"}},
            title={"text": "Business Health Score", "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#FF9900"},
                "bgcolor": "#FFFFFF",
                "borderwidth": 1,
                "bordercolor": "#E6E8EC",
                "steps": [
                    {"range": [0, 60], "color": "rgba(198,40,40,0.16)"},
                    {"range": [60, 80], "color": "rgba(249,168,37,0.18)"},
                    {"range": [80, 100], "color": "rgba(46,125,50,0.16)"},
                ],
            },
        )
    )
    return apply_enterprise_theme(fig, 330)


def feature_importance_bar(importance_df: pd.DataFrame) -> go.Figure:
    """Render model feature importance."""

    top = importance_df.sort_values("importance", ascending=True).tail(10)
    fig = px.bar(
        top,
        x="importance",
        y="feature",
        orientation="h",
        color="importance",
        color_continuous_scale=["#F6F7F9", "#FF9900", "#146EB4"],
        title="Product Success Model Feature Importance",
    )
    return apply_enterprise_theme(fig, 430)


def product_radar(row: pd.Series) -> go.Figure:
    """Render a product score radar chart."""

    metrics = [
        "popularity_index",
        "value_score",
        "customer_trust_index",
        "revenue_opportunity_score",
        "discount_effectiveness_score",
    ]
    values = [float(row[metric]) for metric in metrics]
    labels = [
        "Popularity",
        "Value",
        "Trust",
        "Revenue Upside",
        "Discount Efficiency",
    ]
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                line={"color": "#FF9900", "width": 3},
                fillcolor="rgba(255,153,0,0.24)",
            )
        ]
    )
    fig.update_layout(polar={"radialaxis": {"visible": True, "range": [0, 1]}})
    fig.update_polars(
        bgcolor="#FFFFFF",
        angularaxis={"color": "#475467", "tickfont": {"color": "#475467"}},
        radialaxis={
            "color": "#475467",
            "tickfont": {"color": "#475467"},
            "gridcolor": "#EEF2F6",
        },
    )
    return apply_enterprise_theme(fig, 390)


def discount_waterfall(df: pd.DataFrame) -> go.Figure:
    """Render a waterfall summary of discount opportunity."""

    avg_price = float(df["actual_price_value"].median())
    avg_discounted = float(df["discounted_price_value"].median())
    gap = avg_price - avg_discounted
    fig = go.Figure(
        go.Waterfall(
            measure=["absolute", "relative", "total"],
            x=["Median list price", "Median discount gap", "Median selling price"],
            y=[avg_price, -gap, avg_discounted],
            connector={"line": {"color": "#667085"}},
            increasing={"marker": {"color": "#146EB4"}},
            decreasing={"marker": {"color": "#FF9900"}},
            totals={"marker": {"color": "#2E7D32"}},
        )
    )
    fig.update_layout(title="Pricing Waterfall: List Price to Selling Price")
    return apply_enterprise_theme(fig, 420)
