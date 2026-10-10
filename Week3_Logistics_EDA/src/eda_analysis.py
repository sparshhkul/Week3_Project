"""
Week 3 — Logistics Exploratory Data Analysis and Visualization
Run from the project root:
    pip install -r requirements.txt
    python src/eda_analysis.py

The script reads the supplied DataCo logistics dataset, creates descriptive summaries,
calculates correlations for selected numeric fields, generates visualizations, and
writes an analysis summary for the report.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "DataCo_Logistics_Cleaned.csv"
OUT = ROOT / "outputs"
FIG = OUT / "figures"
REPORTS = ROOT / "reports"
for p in [OUT, FIG, REPORTS]:
    p.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["savefig.dpi"] = 160

def first_existing(columns, candidates):
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None

def savefig(name):
    plt.tight_layout()
    plt.savefig(FIG / name, bbox_inches="tight")
    plt.close()

def main():
    if not INPUT.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT}")
    df = pd.read_csv(INPUT, low_memory=False)
    original_rows, original_cols = df.shape

    # Parse dates for time-based analysis.
    order_date_col = first_existing(df.columns, ["order date (DateOrders)", "Order Date", "order_date"])
    ship_date_col = first_existing(df.columns, ["shipping date (DateOrders)", "Shipping Date", "shipping_date"])
    if order_date_col:
        df[order_date_col] = pd.to_datetime(df[order_date_col], errors="coerce")
    if ship_date_col:
        df[ship_date_col] = pd.to_datetime(df[ship_date_col], errors="coerce")

    # Convert numeric-looking columns only where pandas did not already do so.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    # Descriptive statistics: numeric fields.
    if numeric_cols:
        desc = df[numeric_cols].describe().T.reset_index().rename(columns={"index": "column"})
        desc.to_csv(REPORTS / "numeric_descriptive_statistics.csv", index=False)
    else:
        desc = pd.DataFrame()

    # Data profile summary.
    profile = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_missing": [int(df[c].notna().sum()) for c in df.columns],
        "missing": [int(df[c].isna().sum()) for c in df.columns],
        "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    profile.to_csv(REPORTS / "dataset_profile.csv", index=False)

    # Central tendency table.
    central_rows = []
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s):
            central_rows.append({
                "column": col,
                "mean": float(s.mean()),
                "median": float(s.median()),
                "std": float(s.std()),
                "min": float(s.min()),
                "q1": float(s.quantile(.25)),
                "q3": float(s.quantile(.75)),
                "max": float(s.max()),
                "skewness": float(s.skew()) if s.nunique() > 2 else 0.0
            })
    central = pd.DataFrame(central_rows)
    central.to_csv(REPORTS / "central_tendency_and_spread.csv", index=False)

    # Identify common business columns if available.
    cols = df.columns.tolist()
    delivery_col = first_existing(cols, ["Delivery Status", "Delivery status", "delivery_status"])
    actual_days_col = first_existing(cols, ["Days for shipping (real)", "Actual Shipping Days", "actual_shipping_days"])
    scheduled_days_col = first_existing(cols, ["Days for shipment (scheduled)", "Scheduled Shipping Days", "scheduled_shipping_days"])
    delay_col = first_existing(cols, ["Delivery Delay", "delivery_delay"])
    sales_col = first_existing(cols, ["Sales", "sales"])
    profit_col = first_existing(cols, ["Benefit per order", "Order Profit Per Order", "Order Item Profit Ratio", "Profit", "profit"])
    cost_col = first_existing(cols, ["Order Item Product Price", "Product Price", "Shipping Cost", "shipping_cost"])
    volume_col = first_existing(cols, ["Order Item Quantity", "Order Quantity", "quantity", "Shipment Volume"])
    shipping_mode_col = first_existing(cols, ["Shipping Mode", "shipping_mode"])
    region_col = first_existing(cols, ["Order Region", "Region", "order_region"])
    category_col = first_existing(cols, ["Category Name", "Product Category", "Category", "category"])
    order_id_col = first_existing(cols, ["Order Id", "Order ID", "order_id"])
    delayed_flag_col = first_existing(cols, ["Is Delayed", "is_delayed"])
    late_risk_col = first_existing(cols, ["Late_delivery_risk", "Late Delivery Risk", "late_delivery_risk"])

    # Delivery status distribution.
    if delivery_col:
        counts = df[delivery_col].fillna("Missing").value_counts().head(12)
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(counts)), counts.values); plt.yticks(range(len(counts)), counts.index); plt.gca().invert_yaxis()
        plt.title("Shipment Count by Delivery Status")
        plt.xlabel("Number of records")
        plt.ylabel("Delivery status")
        savefig("01_delivery_status_distribution.png")

    # Shipping time distributions.
    time_cols = [c for c in [actual_days_col, scheduled_days_col] if c]
    if time_cols:
        melted = df[time_cols].melt(var_name="Measure", value_name="Days").dropna()
        plt.figure(figsize=(10, 6))
        sns.histplot(data=melted, x="Days", hue="Measure", element="step", stat="count",
                     common_norm=False, bins=25)
        plt.title("Actual and Scheduled Shipping-Time Distributions")
        plt.xlabel("Shipping time (days)")
        plt.ylabel("Record count")
        savefig("02_shipping_time_distributions.png")

    # Average actual vs scheduled shipping days.
    if actual_days_col and scheduled_days_col:
        means = pd.Series({
            "Actual shipping days": pd.to_numeric(df[actual_days_col], errors="coerce").mean(),
            "Scheduled shipping days": pd.to_numeric(df[scheduled_days_col], errors="coerce").mean()
        })
        plt.figure(figsize=(8, 5))
        plt.bar(range(len(means)), means.values); plt.xticks(range(len(means)), means.index, rotation=10, ha="right")
        plt.title("Average Actual vs Scheduled Shipping Time")
        plt.ylabel("Average days")
        plt.xlabel("")
        savefig("03_average_shipping_time.png")

    # Shipping mode vs average actual duration and/or delivery delay.
    if shipping_mode_col and actual_days_col:
        temp = df[[shipping_mode_col, actual_days_col]].copy()
        temp[actual_days_col] = pd.to_numeric(temp[actual_days_col], errors="coerce")
        mode_avg = temp.groupby(shipping_mode_col, dropna=False)[actual_days_col].mean().sort_values()
        plt.figure(figsize=(9, 5))
        plt.barh(range(len(mode_avg)), mode_avg.values); plt.yticks(range(len(mode_avg)), mode_avg.index); plt.gca().invert_yaxis()
        plt.title("Average Actual Shipping Time by Shipping Mode")
        plt.xlabel("Average actual shipping days")
        plt.ylabel("Shipping mode")
        savefig("04_shipping_mode_performance.png")

    # Monthly order trend.
    if order_date_col:
        monthly = df.dropna(subset=[order_date_col]).set_index(order_date_col).resample("MS").size()
        monthly.rename("order_records").to_csv(REPORTS / "monthly_order_counts.csv", header=True)
        if not monthly.empty:
            plt.figure(figsize=(11, 5))
            sns.lineplot(x=monthly.index, y=monthly.values, marker="o")
            plt.title("Monthly Order-Record Trend")
            plt.xlabel("Order month")
            plt.ylabel("Number of records")
            plt.xticks(rotation=35, ha="right")
            savefig("05_monthly_order_trend.png")

    # Numeric correlation heatmap on meaningful, available metrics.
    corr_candidates = [c for c in [
        actual_days_col, scheduled_days_col, delay_col, sales_col, profit_col,
        cost_col, volume_col, "Order Item Discount", "Order Item Discount Rate",
        "Order Item Total", "Sales per customer", "Order Item Quantity"
    ] if c and c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    corr_candidates = list(dict.fromkeys(corr_candidates))
    corr = pd.DataFrame()
    if len(corr_candidates) >= 2:
        corr = df[corr_candidates].corr(numeric_only=True)
        corr.to_csv(REPORTS / "numeric_correlation_matrix.csv")
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, square=False)
        plt.title("Correlation Between Selected Logistics and Commercial Metrics")
        savefig("06_correlation_heatmap.png")

    # Quantity / sales relationship.
    if volume_col and sales_col:
        temp = df[[volume_col, sales_col]].apply(pd.to_numeric, errors="coerce").dropna()
        if len(temp) > 12000:
            temp = temp.sample(12000, random_state=42)
        plt.figure(figsize=(9, 6))
        sns.scatterplot(data=temp, x=volume_col, y=sales_col, alpha=.35, s=20)
        plt.title("Relationship Between Item Quantity and Sales")
        plt.xlabel(volume_col)
        plt.ylabel(sales_col)
        savefig("07_quantity_vs_sales.png")

    # Top regions by record count.
    if region_col:
        region_counts = df[region_col].fillna("Missing").value_counts().head(12)
        region_counts.rename_axis("region").reset_index(name="records").to_csv(
            REPORTS / "top_regions_by_records.csv", index=False)
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(region_counts)), region_counts.values); plt.yticks(range(len(region_counts)), region_counts.index); plt.gca().invert_yaxis()
        plt.title("Top Regions by Logistics Record Count")
        plt.xlabel("Number of records")
        plt.ylabel("Order region")
        savefig("08_top_regions.png")

    # Product category volume.
    if category_col:
        category_counts = df[category_col].fillna("Missing").value_counts().head(12)
        category_counts.rename_axis("category").reset_index(name="records").to_csv(
            REPORTS / "category_record_counts.csv", index=False)
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(category_counts)), category_counts.values); plt.yticks(range(len(category_counts)), category_counts.index); plt.gca().invert_yaxis()
        plt.title("Top Product Categories by Record Count")
        plt.xlabel("Number of records")
        plt.ylabel("Product category")
        savefig("09_category_record_counts.png")

    # Delay status by shipping mode.
    if shipping_mode_col and (delayed_flag_col or late_risk_col):
        flag = delayed_flag_col or late_risk_col
        temp = df[[shipping_mode_col, flag]].copy()
        temp[flag] = pd.to_numeric(temp[flag], errors="coerce")
        rate = temp.groupby(shipping_mode_col)[flag].mean().sort_values(ascending=False) * 100
        rate.rename("flag_percent").to_csv(REPORTS / "delay_flag_rate_by_shipping_mode.csv", header=True)
        plt.figure(figsize=(9, 5))
        plt.barh(range(len(rate)), rate.values); plt.yticks(range(len(rate)), rate.index); plt.gca().invert_yaxis()
        plt.title(f"Mean {flag} Value by Shipping Mode (percentage only if binary)")
        plt.xlabel(f"Mean {flag} value × 100")
        plt.ylabel("Shipping mode")
        savefig("10_delay_flag_by_shipping_mode.png")

    # Summarized statistics used in report.
    summary = {
        "input_file": INPUT.name,
        "rows": int(original_rows),
        "columns": int(original_cols),
        "missing_cells": int(df.isna().sum().sum()),
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "date_columns": {"order_date": order_date_col, "shipping_date": ship_date_col},
        "business_columns": {
            "delivery_status": delivery_col, "actual_days": actual_days_col,
            "scheduled_days": scheduled_days_col, "delay": delay_col, "sales": sales_col,
            "profit_or_benefit": profit_col, "cost_or_price": cost_col, "quantity": volume_col,
            "shipping_mode": shipping_mode_col, "region": region_col, "category": category_col,
            "order_id": order_id_col, "delay_flag": delayed_flag_col, "late_risk_flag": late_risk_col
        },
        "figures_created": sorted([p.name for p in FIG.glob("*.png")]),
    }

    # Add key descriptive values and actual-vs-scheduled comparison.
    if actual_days_col:
        actual = pd.to_numeric(df[actual_days_col], errors="coerce")
        summary["actual_shipping_days"] = {
            "mean": float(actual.mean()), "median": float(actual.median()),
            "std": float(actual.std()), "min": float(actual.min()), "max": float(actual.max())
        }
    if scheduled_days_col:
        sched = pd.to_numeric(df[scheduled_days_col], errors="coerce")
        summary["scheduled_shipping_days"] = {
            "mean": float(sched.mean()), "median": float(sched.median()),
            "std": float(sched.std()), "min": float(sched.min()), "max": float(sched.max())
        }
    if actual_days_col and scheduled_days_col:
        actual = pd.to_numeric(df[actual_days_col], errors="coerce")
        sched = pd.to_numeric(df[scheduled_days_col], errors="coerce")
        summary["mean_shipping_time_gap_days"] = float((actual - sched).mean())
        summary["records_actual_exceeds_schedule"] = int((actual > sched).sum())
        summary["records_actual_at_or_below_schedule"] = int((actual <= sched).sum())
    if delivery_col:
        summary["delivery_status_counts"] = {str(k): int(v) for k, v in df[delivery_col].value_counts(dropna=False).items()}
    if shipping_mode_col and actual_days_col:
        summary["mean_actual_days_by_shipping_mode"] = {
            str(k): float(v) for k, v in df.groupby(shipping_mode_col)[actual_days_col].mean().sort_values().items()
        }
    if sales_col:
        s = pd.to_numeric(df[sales_col], errors="coerce")
        summary["sales"] = {"mean": float(s.mean()), "median": float(s.median()), "sum": float(s.sum())}
    if volume_col:
        s = pd.to_numeric(df[volume_col], errors="coerce")
        summary["quantity"] = {"mean": float(s.mean()), "median": float(s.median()), "sum": float(s.sum())}
    (REPORTS / "eda_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
