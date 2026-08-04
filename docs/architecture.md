# Architecture

The Amazon Product Intelligence Platform is organized as a modular analytics system.

## Layers

- `data/raw`: immutable source extracts.
- `src/preprocessing.py`: parsing, typing, and cleaning functions.
- `src/data_quality.py`: schema validation, anomaly checks, and quality scorecards.
- `src/feature_engineering.py`: business features such as value score, trust index, and priority score.
- `src/analytics.py`: executive KPIs, category performance, pricing actions, and product recommendations.
- `src/statistics.py`: hypothesis tests and correlation analysis.
- `src/modeling.py`: success classification and product segmentation.
- `src/recommendation.py`: TF-IDF content-based recommendations.
- `src/visualization.py`: reusable chart generation.
- `src/pipeline.py`: thin orchestration layer that calls the modules.
- `app/streamlit_app.py`: executive analytics application.

## Design Decision

Business logic is intentionally split across separate files. This makes the repository easier to learn, test, extend, and explain in interviews.

