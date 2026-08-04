"""Machine learning models for product success and segmentation."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

MODEL_FEATURES = [
    "discounted_price_value",
    "actual_price_value",
    "discount_rate",
    "rating_value",
    "rating_count_value",
    "weighted_rating",
    "bayesian_rating",
    "price_competitiveness_index",
    "discount_effectiveness_score",
    "customer_trust_index",
    "revenue_opportunity_score",
]


def train_success_classifier(
    df: pd.DataFrame, model_path: Path, random_state: int = 42
) -> dict[str, object]:
    """Train a product success classifier and save the fitted model."""

    model_data = df[MODEL_FEATURES + ["success_label"]].dropna()
    x = model_data[MODEL_FEATURES]
    y = model_data["success_label"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=random_state, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=8,
        min_samples_leaf=5,
        random_state=random_state,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    importances = pd.DataFrame(
        {"feature": MODEL_FEATURES, "importance": model.feature_importances_}
    ).sort_values("importance", ascending=False)
    return {
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "classification_report": classification_report(y_test, predictions, output_dict=True),
        "feature_importance": importances,
    }


def segment_products(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
    """Cluster products into business segments."""

    features = [
        "popularity_index",
        "value_score",
        "customer_trust_index",
        "revenue_opportunity_score",
        "discount_effectiveness_score",
    ]
    pipeline = Pipeline(
        [("scaler", StandardScaler()), ("kmeans", KMeans(n_clusters=4, n_init=20, random_state=random_state))]
    )
    segments = df[["product_id", "product_name", "primary_category"] + features].copy()
    segments["segment"] = pipeline.fit_predict(segments[features])
    labels = _label_segments(segments)
    segments["segment_name"] = segments["segment"].map(labels)
    return segments


def _label_segments(segments: pd.DataFrame) -> dict[int, str]:
    summary = segments.groupby("segment")[
        ["customer_trust_index", "revenue_opportunity_score", "popularity_index"]
    ].mean()
    labels: dict[int, str] = {}
    for segment, row in summary.iterrows():
        if row.customer_trust_index == summary["customer_trust_index"].max():
            labels[segment] = "Trusted Winners"
        elif row.revenue_opportunity_score == summary["revenue_opportunity_score"].max():
            labels[segment] = "Revenue Upside"
        elif row.popularity_index == summary["popularity_index"].min():
            labels[segment] = "Visibility Builders"
        else:
            labels[segment] = "Margin Watchlist"
    return labels

