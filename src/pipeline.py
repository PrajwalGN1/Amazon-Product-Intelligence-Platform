"""Thin orchestration pipeline for the modular analytics platform."""

from __future__ import annotations

from src.analytics import category_performance, executive_kpis, pricing_opportunities, product_priority_table
from src.config import CONFIG
from src.data_quality import calculate_quality_score, run_quality_rules, validate_schema
from src.feature_engineering import add_business_features
from src.modeling import segment_products, train_success_classifier
from src.preprocessing import clean_product_data, load_raw_data
from src.statistics import discount_rating_hypothesis, numeric_correlations
from src.utilities import ensure_directories, save_dataframe, save_json
from src.visualization import save_category_priority_chart, save_price_rating_chart


def run_pipeline() -> None:
    """Execute the end-to-end reproducible analytics workflow."""

    ensure_directories(
        CONFIG.processed_dir,
        CONFIG.validation_dir,
        CONFIG.reports_dir,
        CONFIG.images_dir,
        CONFIG.models_dir,
    )
    raw = load_raw_data(CONFIG.raw_data_path)
    schema_report = validate_schema(raw)
    clean = clean_product_data(raw)
    featured = add_business_features(clean)
    scorecard = run_quality_rules(featured)
    quality_score = calculate_quality_score(scorecard, len(featured))
    category_df = category_performance(featured)
    priority_df = product_priority_table(featured)
    pricing_df = pricing_opportunities(featured)
    stats_df = discount_rating_hypothesis(featured)
    corr_df = numeric_correlations(featured)
    segments_df = segment_products(featured, CONFIG.random_state)
    model_report = train_success_classifier(
        featured, CONFIG.models_dir / "product_success_random_forest.joblib", CONFIG.random_state
    )

    save_dataframe(featured, CONFIG.processed_dir / "amazon_products_featured.csv")
    save_dataframe(scorecard, CONFIG.validation_dir / "data_quality_scorecard.csv")
    save_dataframe(category_df, CONFIG.reports_dir / "category_performance.csv")
    save_dataframe(priority_df, CONFIG.reports_dir / "product_priority_recommendations.csv")
    save_dataframe(pricing_df, CONFIG.reports_dir / "pricing_opportunities.csv")
    save_dataframe(stats_df, CONFIG.reports_dir / "statistical_tests.csv")
    save_dataframe(corr_df, CONFIG.reports_dir / "numeric_correlations.csv")
    save_dataframe(segments_df, CONFIG.reports_dir / "product_segments.csv")
    save_dataframe(model_report["feature_importance"], CONFIG.reports_dir / "model_feature_importance.csv")
    save_json(
        {
            "executive_kpis": executive_kpis(featured),
            "schema_report": schema_report,
            "quality_score": quality_score,
            "model_roc_auc": model_report["roc_auc"],
            "business_recommendations": [
                "Prioritize promotions for products with high trust, strong review volume, and revenue upside.",
                "Audit aggressive discounts where customer ratings remain below 4.0.",
                "Treat low-review products as visibility experiments before committing major ad spend.",
                "Use category scorecards to protect strong categories and diagnose underperforming ones.",
            ],
        },
        CONFIG.reports_dir / "executive_summary.json",
    )
    save_category_priority_chart(category_df, CONFIG.images_dir / "category_priority_score.png")
    save_price_rating_chart(featured, CONFIG.images_dir / "price_rating_discount.png")


if __name__ == "__main__":
    run_pipeline()

