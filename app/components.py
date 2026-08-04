"""Reusable Streamlit UI components."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import pandas as pd
import streamlit as st


def render_top_nav(data_version: str, model_version: str) -> None:
    """Render the executive product header."""

    now = datetime.now()
    st.markdown(
        f"""
        <div class="top-nav">
            <div class="brand-lockup">
                <div class="brand-mark">PI</div>
                <div>
                    <p class="brand-title">Amazon Product Intelligence Platform</p>
                    <div class="brand-subtitle">Executive Decision Intelligence Dashboard</div>
                </div>
            </div>
            <div class="status-strip">
                <span class="status-pill">{now:%d %b %Y}</span>
                <span class="status-pill">{now:%I:%M %p}</span>
                <span class="status-pill status-ok">System Online</span>
                <span class="status-pill status-ok">Pipeline Ready</span>
                <span class="status-pill">{data_version}</span>
                <span class="status-pill">{model_version}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(products: int, categories: int, quality_score: float) -> None:
    """Render the landing page hero section."""

    st.markdown(
        f"""
        <div class="hero">
            <span class="badge">Executive command center</span>
            <h1>Product decisions powered by pricing, trust, demand and recommendation intelligence.</h1>
            <p>
                A premium decision layer for identifying promotion candidates, pricing risks,
                category opportunities, and product-level actions across the Amazon catalog.
            </p>
            <div class="hero-grid">
                <div class="hero-chip"><b>{products:,}</b><br/>Products analyzed</div>
                <div class="hero-chip"><b>{categories:,}</b><br/>Category groups monitored</div>
                <div class="hero-chip"><b>{quality_score:.2f}</b><br/>Data quality score</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(
    label: str,
    value: str,
    change: str,
    status: str,
    icon: str,
    bars: Iterable[int],
) -> None:
    """Render a custom KPI card."""

    sparkline = "".join(
        f'<span style="height:{max(4, int(height))}px"></span>' for height in bars
    )
    st.markdown(
        f"""
        <div class="card metric-card">
            <div class="metric-top">
                <div class="metric-icon">{icon}</div>
                <span class="badge status-ok">{status}</span>
            </div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-change">{change}</div>
            <div class="sparkline">{sparkline}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str) -> None:
    """Render a consistent section title."""

    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-kicker">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_panel(title: str, body: str) -> None:
    """Render a styled sidebar information panel."""

    st.sidebar.markdown(
        f"""
        <div class="sidebar-card">
            <b>{title}</b>
            <div style="color:#667085;font-size:0.82rem;margin-top:0.35rem;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(
    observation: str,
    implication: str,
    recommendation: str,
    priority: str,
    impact: str,
) -> None:
    """Render an executive insight card."""

    priority_class = "priority-high" if priority == "High" else "priority-medium"
    st.markdown(
        f"""
        <div class="card insight-card">
            <span class="badge {priority_class}">{priority} priority</span>
            <h4 style="margin:0.65rem 0 0.35rem;color:#232F3E;">{observation}</h4>
            <p><b>Business implication:</b> {implication}</p>
            <p><b>Recommendation:</b> {recommendation}</p>
            <p><b>Expected impact:</b> {impact}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def product_card(row: pd.Series) -> None:
    """Render an Amazon-inspired recommendation card."""

    title = str(row["product_name"])[:120]
    price = f"Rs. {row['discounted_price_value']:,.0f}"
    discount = f"{row['discount_rate']:.0%} off"
    score = float(row.get("similarity_score", row.get("business_priority_score", 0)))
    st.markdown(
        f"""
        <div class="card product-card">
            <img src="{row['img_link']}" alt="Product image"/>
            <div>
                <div style="font-weight:800;color:#232F3E;">{title}</div>
                <div style="color:#667085;font-size:0.82rem;margin:0.25rem 0;">{row['primary_category']}</div>
                <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:0.45rem 0;">
                    <span class="badge">Rating {row['rating_value']:.1f}</span>
                    <span class="badge">{price}</span>
                    <span class="badge status-ok">{discount}</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:{min(score * 100, 100):.0f}%"></div>
                </div>
                <div style="font-size:0.76rem;color:#667085;margin-top:0.25rem;">Recommendation confidence {score:.2f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_priority_table(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """Apply conditional formatting to executive tables."""

    numeric_cols = [
        column
        for column in df.columns
        if df[column].dtype.kind in "if" and "id" not in column.lower()
    ]
    styler = df.style
    if numeric_cols:
        styler = styler.background_gradient(subset=numeric_cols, cmap="YlGnBu")
    return styler.format(precision=3)

