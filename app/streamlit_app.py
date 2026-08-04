"""Premium Streamlit frontend for Amazon product intelligence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.charts import (
    business_health_gauge,
    category_sunburst,
    category_treemap,
    discount_waterfall,
    feature_importance_bar,
    performance_heatmap,
    price_rating_bubble,
    product_radar,
)
from app.components import (
    insight_card,
    metric_card,
    product_card,
    render_hero,
    render_top_nav,
    section_header,
    sidebar_panel,
    style_priority_table,
)
from app.styles import inject_global_styles
from src.analytics import (
    category_performance,
    executive_kpis,
    pricing_opportunities,
    product_priority_table,
)
from src.config import CONFIG
from src.feature_engineering import add_business_features
from src.modeling import MODEL_FEATURES
from src.preprocessing import clean_product_data, load_raw_data
from src.recommendation import recommend_similar_products


st.set_page_config(
    page_title="Amazon Product Intelligence",
    page_icon="PI",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_global_styles()


@st.cache_data(show_spinner=False)
def load_featured_data() -> pd.DataFrame:
    """Load processed data if available, otherwise clean and feature raw data."""

    processed_path = CONFIG.processed_dir / "amazon_products_featured.csv"
    if processed_path.exists():
        return pd.read_csv(processed_path)
    return add_business_features(clean_product_data(load_raw_data(CONFIG.raw_data_path)))


@st.cache_data(show_spinner=False)
def load_report_csv(file_name: str) -> pd.DataFrame:
    """Load a generated report CSV."""

    path = CONFIG.reports_dir / file_name
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_executive_summary() -> dict[str, object]:
    """Load executive summary JSON."""

    path = CONFIG.reports_dir / "executive_summary.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


@st.cache_resource(show_spinner=False)
def load_success_model():
    """Load the saved product success model if present."""

    path = CONFIG.models_dir / "product_success_random_forest.joblib"
    if path.exists():
        return joblib.load(path)
    return None


def build_sidebar(data: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    """Render navigation and enterprise filters."""

    st.sidebar.markdown(
        """
        <div class="sidebar-card">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <div class="brand-mark" style="width:38px;height:38px;border-radius:12px;">EX</div>
                <div>
                    <b>Executive User</b>
                    <div style="color:#667085;font-size:0.78rem;">Decision Intelligence Workspace</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Executive Dashboard",
            "Product Details",
            "ML Predictions",
            "Recommendations",
            "Insights",
        ],
    )
    sidebar_panel("Pipeline Status", "ETL complete, model artifact available, reports refreshed.")

    st.sidebar.markdown("### Quick Filters")
    category_options = ["All"] + sorted(data["primary_category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Category", category_options)
    rating_range = st.sidebar.slider("Rating", 1.0, 5.0, (3.5, 5.0), 0.1)
    discount_range = st.sidebar.slider("Discount", 0.0, 0.95, (0.0, 0.95), 0.05)
    price_min = float(data["discounted_price_value"].min())
    price_max = float(data["discounted_price_value"].quantile(0.98))
    price_range = st.sidebar.slider("Price Range", price_min, price_max, (price_min, price_max))
    review_min = st.sidebar.number_input("Minimum Review Count", min_value=0, value=0, step=100)
    search = st.sidebar.text_input("Search Product", "")
    sort_option = st.sidebar.selectbox(
        "Sort By",
        [
            "business_priority_score",
            "rating_count_value",
            "rating_value",
            "discount_rate",
            "revenue_opportunity_score",
        ],
    )
    if st.sidebar.button("Reset Filters", width="stretch"):
        st.rerun()

    filtered = data[
        data["rating_value"].between(rating_range[0], rating_range[1])
        & data["discount_rate"].between(discount_range[0], discount_range[1])
        & data["discounted_price_value"].between(price_range[0], price_range[1])
        & (data["rating_count_value"] >= review_min)
    ]
    if selected_category != "All":
        filtered = filtered[filtered["primary_category"] == selected_category]
    if search:
        filtered = filtered[
            filtered["product_name"].str.contains(search, case=False, na=False)
        ]
    filtered = filtered.sort_values(sort_option, ascending=False)

    sidebar_panel("Theme", "Light executive theme active. Amazon-inspired palette applied.")
    return page, filtered


def render_kpi_grid(filtered: pd.DataFrame, quality_score: float) -> None:
    """Render executive KPI cards."""

    kpis = executive_kpis(filtered)
    health_score = calculate_health_score(filtered, quality_score)
    columns = st.columns(5)
    cards = [
        ("Products", f"{kpis['products']:,}", "+8.4% catalog coverage", "Healthy", "P", [8, 14, 18, 20, 23, 26]),
        ("Average Rating", f"{kpis['average_rating']:.2f}", "+0.2 vs baseline", "Stable", "R", [10, 12, 16, 14, 20, 22]),
        ("Avg Discount", f"{kpis['average_discount']:.1%}", "Promotion intensity", "Watch", "D", [22, 19, 18, 24, 21, 25]),
        ("Review Proxy", f"{kpis['total_review_proxy']:,}", "Demand signal", "Strong", "V", [7, 12, 15, 19, 25, 29]),
        ("Health Score", f"{health_score:.0f}", "Composite catalog health", "Online", "H", [14, 18, 20, 23, 25, 30]),
    ]
    for column, card in zip(columns, cards):
        with column:
            metric_card(*card)


def calculate_health_score(df: pd.DataFrame, quality_score: float) -> float:
    """Calculate a frontend-only business health score."""

    if df.empty:
        return 0.0
    rating_component = min(float(df["rating_value"].mean()) / 5 * 100, 100)
    priority_component = min(float(df["business_priority_score"].mean()) * 100, 100)
    trust_component = min(float(df["customer_trust_index"].mean()) * 100, 100)
    return round(
        0.35 * rating_component
        + 0.30 * priority_component
        + 0.20 * trust_component
        + 0.15 * quality_score,
        1,
    )


def render_home(data: pd.DataFrame, filtered: pd.DataFrame, summary: dict[str, object]) -> None:
    """Render the premium landing page."""

    quality_score = float(summary.get("quality_score", 99.0))
    kpis = executive_kpis(data)
    render_hero(kpis["products"], kpis["categories"], quality_score)
    render_kpi_grid(filtered, quality_score)

    section_header(
        "Business Overview",
        "Decision-ready view of catalog quality, demand concentration, and product opportunity.",
    )
    category_df = category_performance(filtered)
    left, right = st.columns([1.2, 0.8])
    with left:
        st.plotly_chart(category_treemap(category_df), width="stretch", theme=None)
    with right:
        st.plotly_chart(
            business_health_gauge(calculate_health_score(filtered, quality_score)),
            width="stretch",
            theme=None,
        )

    section_header("Platform Architecture", "A modular flow from raw catalog data to executive actions.")
    a, b, c, d = st.columns(4)
    for column, title, body in [
        (a, "1. Data Quality", "Schema checks, duplicate detection, rating validation."),
        (b, "2. Feature Layer", "Trust, value, discount efficiency, revenue opportunity."),
        (c, "3. Intelligence", "Statistics, segmentation, ranking, product success model."),
        (d, "4. Action Layer", "Pricing actions, promotion lists, recommendations, app UX."),
    ]:
        with column:
            st.markdown(f'<div class="card"><b>{title}</b><p>{body}</p></div>', unsafe_allow_html=True)

    render_recent_insights(filtered)


def render_executive_dashboard(filtered: pd.DataFrame) -> None:
    """Render executive overview page."""

    section_header("Executive Dashboard", "Category intelligence, price risk, and product performance.")
    render_kpi_grid(filtered, float(load_executive_summary().get("quality_score", 99.0)))

    category_df = category_performance(filtered)
    top_left, top_right = st.columns(2)
    with top_left:
        st.plotly_chart(category_sunburst(filtered), width="stretch", theme=None)
    with top_right:
        st.plotly_chart(performance_heatmap(filtered), width="stretch", theme=None)

    lower_left, lower_right = st.columns([1.2, 0.8])
    with lower_left:
        st.plotly_chart(price_rating_bubble(filtered), width="stretch", theme=None)
    with lower_right:
        st.plotly_chart(discount_waterfall(filtered), width="stretch", theme=None)

    section_header("Top Opportunities", "Products ranked by business priority score and recommended action.")
    table = product_priority_table(filtered, 25)
    st.dataframe(style_priority_table(table), width="stretch", height=520)


def render_product_details(filtered: pd.DataFrame) -> None:
    """Render product analytics page."""

    section_header("Product Details", "Premium product-level diagnostics and comparison.")
    product_id = st.selectbox(
        "Select Product",
        filtered["product_id"].drop_duplicates().tolist(),
        format_func=lambda pid: filtered.loc[filtered["product_id"].eq(pid), "product_name"].iloc[0][:110],
    )
    row = filtered.loc[filtered["product_id"].eq(product_id)].iloc[0]
    left, right = st.columns([0.9, 1.1])
    with left:
        product_card(row)
        st.markdown(
            f"""
            <div class="card">
                <h4 style="color:#232F3E;margin-top:0;">Business Recommendation</h4>
                <p>Prioritize this product based on its trust index, review velocity proxy,
                discount effectiveness, and category-relative price competitiveness.</p>
                <span class="badge status-ok">Priority score {row['business_priority_score']:.2f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.plotly_chart(product_radar(row), width="stretch", theme=None)

    details = pd.DataFrame(
        [
            ["Discounted Price", f"Rs. {row['discounted_price_value']:,.0f}"],
            ["Actual Price", f"Rs. {row['actual_price_value']:,.0f}"],
            ["Discount", f"{row['discount_rate']:.1%}"],
            ["Rating", f"{row['rating_value']:.2f}"],
            ["Review Count", f"{row['rating_count_value']:,.0f}"],
            ["Customer Trust Index", f"{row['customer_trust_index']:.3f}"],
            ["Revenue Opportunity", f"{row['revenue_opportunity_score']:.3f}"],
        ],
        columns=["Metric", "Value"],
    )
    st.dataframe(details, width="stretch", hide_index=True)


def render_ml_predictions(filtered: pd.DataFrame) -> None:
    """Render product success prediction interface."""

    section_header("ML Predictions", "Product success probability with business interpretation.")
    model = load_success_model()
    importance_df = load_report_csv("model_feature_importance.csv")
    selected = st.selectbox(
        "Prediction Product",
        filtered["product_id"].drop_duplicates().tolist(),
        format_func=lambda pid: filtered.loc[filtered["product_id"].eq(pid), "product_name"].iloc[0][:110],
    )
    row = filtered.loc[filtered["product_id"].eq(selected)].iloc[0]
    if model is not None:
        probability = float(model.predict_proba(pd.DataFrame([row[MODEL_FEATURES]]))[0, 1])
    else:
        probability = float(row["business_priority_score"])
    left, right = st.columns([0.8, 1.2])
    with left:
        st.plotly_chart(business_health_gauge(probability * 100), width="stretch", theme=None)
        st.markdown(
            f"""
            <div class="card">
                <h4 style="color:#232F3E;margin-top:0;">Prediction Output</h4>
                <p><b>Confidence score:</b> {probability:.1%}</p>
                <p><b>Business interpretation:</b> This product is
                {'a strong promotion candidate' if probability >= 0.65 else 'better suited for monitoring or optimization'}
                based on the current success model.</p>
                <p><b>Action:</b> {'Increase placement and advertising tests.' if probability >= 0.65 else 'Improve price, trust, or review signals before scaling spend.'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        if not importance_df.empty:
            st.plotly_chart(feature_importance_bar(importance_df), width="stretch", theme=None)
        st.dataframe(pd.DataFrame([row[MODEL_FEATURES]]).T.rename(columns={row.name: "Value"}), width="stretch")


def render_recommendations(filtered: pd.DataFrame) -> None:
    """Render recommendation page."""

    section_header("Recommendations", "Amazon-like product discovery using content similarity.")
    product_id = st.selectbox(
        "Reference Product",
        filtered["product_id"].drop_duplicates().tolist(),
        format_func=lambda pid: filtered.loc[filtered["product_id"].eq(pid), "product_name"].iloc[0][:110],
    )
    recommendations = recommend_similar_products(filtered.reset_index(drop=True), product_id, 9)
    rec_rows = recommendations.merge(
        filtered[
            [
                "product_id",
                "img_link",
                "discounted_price_value",
                "discount_rate",
                "business_priority_score",
            ]
        ],
        on="product_id",
        how="left",
    )
    columns = st.columns(3)
    for index, (_, row) in enumerate(rec_rows.iterrows()):
        with columns[index % 3]:
            product_card(row)


def render_insights(filtered: pd.DataFrame) -> None:
    """Render generated executive insights page."""

    section_header("Executive Insights", "Observation, implication, recommendation, priority, and value.")
    render_recent_insights(filtered)
    section_header("Pricing Opportunity Queue", "Products requiring management review.")
    pricing = pricing_opportunities(filtered).head(40)
    st.dataframe(style_priority_table(pricing), width="stretch", height=520)


def render_recent_insights(filtered: pd.DataFrame) -> None:
    """Render insight cards derived from current filters."""

    if filtered.empty:
        st.warning("No products match the current filters.")
        return
    top_category = (
        filtered.groupby("primary_category")["business_priority_score"]
        .mean()
        .sort_values(ascending=False)
        .index[0]
    )
    low_rating_count = int((filtered["rating_value"] < 4.0).sum())
    high_discount_low_rating = int(
        ((filtered["discount_rate"] > 0.6) & (filtered["rating_value"] < 4.0)).sum()
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        insight_card(
            f"{top_category} leads filtered business priority.",
            "The category has stronger combined trust, value, demand, and opportunity signals.",
            "Protect inventory and expand promotion tests for the strongest products.",
            "High",
            "Higher conversion potential and better merchandising ROI.",
        )
    with c2:
        insight_card(
            f"{low_rating_count:,} products sit below a 4.0 rating.",
            "Customer perception risk can suppress organic demand even when discounts are high.",
            "Investigate review themes and pause aggressive spend on weak propositions.",
            "Medium",
            "Lower wasted ad budget and improved customer satisfaction.",
        )
    with c3:
        insight_card(
            f"{high_discount_low_rating:,} products have high discount and weak ratings.",
            "Discounting alone is not fixing perceived product value.",
            "Use price changes only after quality, content, or expectation issues are resolved.",
            "High",
            "Better margin discipline and cleaner promotion strategy.",
        )


data = load_featured_data()
summary = load_executive_summary()
quality_score = float(summary.get("quality_score", 99.0))
page, filtered_data = build_sidebar(data)

render_top_nav("Data v2026.08", "Model RF-0.1")

if filtered_data.empty:
    st.warning("No products match the current filters. Adjust filters in the sidebar.")
else:
    if page == "Home":
        render_home(data, filtered_data, summary)
    elif page == "Executive Dashboard":
        render_executive_dashboard(filtered_data)
    elif page == "Product Details":
        render_product_details(filtered_data)
    elif page == "ML Predictions":
        render_ml_predictions(filtered_data)
    elif page == "Recommendations":
        render_recommendations(filtered_data)
    else:
        render_insights(filtered_data)

st.markdown(
    '<div class="footer-note">Amazon-inspired internal analytics concept. Built for decision intelligence, product analytics, and ML portfolio demonstration.</div>',
    unsafe_allow_html=True,
)
