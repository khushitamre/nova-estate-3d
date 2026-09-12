# NOVA / ESTATE 3D

## Residential market intelligence, explored in three dimensions

NOVA / ESTATE 3D is a completely redesigned Streamlit portfolio project built from the Ames Housing dataset. It is not a long dashboard with many pages. It is a focused product experience with three short views and one memorable interaction: a rotatable 3D price landscape.

## Product concept

The interface treats exploratory data analysis as an intelligence product. Three spatial dimensions show living area, overall quality, and sale price. Garage capacity is encoded as marker size, while hover context exposes neighborhood, year built, and sale year.

## The three views

| View | Purpose |
|---|---|
| **01 · Orbit / 3D Market** | Rotate the 3D market orbit and inspect how living area, quality, and price meet. |
| **02 · Signal Lab** | Create a transparent hypothetical profile and inspect the strongest observed price signals. |
| **03 · Evidence Room** | Review the area-price relationship, locality ranking, and expandable data-quality audit. |

The product is intentionally streamlined. It avoids an endless scroll and keeps the primary story visible within three compact views.

## Requirements covered

| Assessment requirement | NOVA implementation |
|---|---|
| Ames Housing data | Bundled real dataset in `data/ames_housing.csv` |
| Explore columns | Data-quality audit and interactive exploration |
| Missing values | Median/mode imputation or drop-incomplete-rows option |
| Basic statistics | KPI strip, driver ranking, locality table |
| Price distribution | Market KPIs and evidence view |
| Price vs area | Interactive scatter with NumPy linear trendline |
| Price by locality | Neighborhood ranking bar chart |
| Correlation heatmap | Target correlation logic used for driver ranking |
| Three strongest predictors | Signal Constellation cards and ranked bar chart |
| Short summary | Signal Lab explanation and evidence-room presentation |
| Premium interactive UI | Obsidian Aurora theme, rotatable 3D chart, three-view navigation |

## Key findings

| Rank | Feature | Pearson correlation with SalePrice |
|---:|---|---:|
| 1 | `Overall_Qual` | 0.799 |
| 2 | `Gr_Liv_Area` | 0.707 |
| 3 | `Garage_Cars` | 0.648 |

These are linear associations, not causal effects or a production appraisal.

## Run locally

From the extracted project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open `http://localhost:8501`.

The app first loads `data/ames_housing.csv`. If a GitHub clone is missing that folder, it automatically downloads the reproducible Ames Housing CSV from the configured public source and stores it in `data/` for the current run. For a fully offline run, keep the CSV in the repository at `data/ames_housing.csv`.

The project intentionally does not require `statsmodels`. The linear trendline uses NumPy, which keeps installation simpler and avoids the earlier missing-module error.

## Project structure

```text
house-price-eda/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── ames_housing.csv
└── assets/
    └── nova-3d-overview.webp
```

## References

[1]: https://github.com/wblakecannon/ames/blob/master/data/housing.csv "Ames Housing dataset CSV"
[2]: https://inria.github.io/scikit-learn-mooc/python_scripts/datasets_ames_housing.html "The Ames housing dataset — Scikit-learn MOOC"
