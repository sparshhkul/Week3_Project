# Week 3 — Logistics Exploratory Data Analysis (EDA)

## Dataset
The project uses the supplied `DataCo_Logistics_Cleaned.csv` from the Week 1/Week 2 workflow.

## Run instructions
1. Install Python 3.10 or newer.
2. In a terminal, move to this folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python src/eda_analysis.py`

## Generated outputs
- `outputs/figures/` — charts created by the EDA script.
- `reports/eda_summary.json` — main numerical findings.
- `reports/dataset_profile.csv` — data types, missing counts, and unique values.
- `reports/central_tendency_and_spread.csv` — mean, median, standard deviation, quartiles, range, and skewness.
- `reports/numeric_descriptive_statistics.csv` — pandas descriptive statistics.
- `reports/numeric_correlation_matrix.csv` — selected numeric correlations, if at least two eligible columns exist.
- Additional CSV reports for monthly orders, top regions/categories, and delay flags where applicable.

## Notes
This is exploratory analysis, not causal inference. A correlation does not prove that one metric causes another. The data is an order/item-level dataset, so record counts should not automatically be described as unique shipments unless the relevant identifiers confirm that.
