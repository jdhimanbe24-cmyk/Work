"""
main.py
========
E-commerce Sales Analysis — Week 4 Data Analysis Project

A complete, self-contained pipeline that:
  1. Loads raw sales data from data/sales_data.csv
  2. Cleans it (handles missing values, invalid entries, duplicates)
  3. Analyzes it (totals, averages, top performers, trends)
  4. Visualizes it (bar chart, line chart, pie chart)
  5. Writes a report with the numeric findings and written insights

Dataset columns: Date, Product, Quantity, Price, Customer_ID, Region, Total_Sales

Run with:
    python main.py

Outputs:
    visualizations/sales_by_product.png
    visualizations/monthly_sales_trend.png
    visualizations/sales_share_by_region.png
    report/analysis_report.md
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuration / paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
REPORT_DIR = os.path.join(BASE_DIR, "report")

os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")

REQUIRED_COLUMNS = ["Date", "Product", "Quantity", "Price", "Region", "Total_Sales"]


# ---------------------------------------------------------------------------
# Step 1: Load data
# ---------------------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    """Load the CSV file, with error handling for common problems."""
    if not os.path.exists(path):
        print(f"ERROR: Data file not found at {path}")
        sys.exit(1)
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        print("ERROR: The data file is empty.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read data file. Details: {e}")
        sys.exit(1)

    if df.empty:
        print("ERROR: No rows found in the dataset.")
        sys.exit(1)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        print(f"ERROR: Dataset is missing required column(s): {missing_cols}")
        sys.exit(1)

    print(f"Loaded {len(df)} rows from {os.path.basename(path)}")
    return df


# ---------------------------------------------------------------------------
# Step 2: Clean data
# ---------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning steps performed (and why):
      - Parse Date column to real datetime objects (needed for the trend chart)
      - Drop exact duplicate rows (data entry duplicates)
      - Drop rows with missing Quantity, Price, or Total_Sales
        (can't analyze an incomplete sale)
      - Drop rows with negative/zero Quantity, Price, or Total_Sales (invalid entries)
      - Flag rows where Total_Sales doesn't match Quantity * Price
        (a common data-entry error) rather than silently trusting the raw column
      - Reset the index after dropping rows
    Note: this dataset arrived clean, so most steps below report 0 removed — they
    are kept in place so the pipeline is robust against messier data too.
    """
    original_count = len(df)
    report_lines = []

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    report_lines.append(f"Removed {duplicates} duplicate row(s).")

    numeric_cols = ["Quantity", "Price", "Total_Sales"]
    missing_before = df[numeric_cols + ["Date"]].isna().sum().sum()
    df = df.dropna(subset=numeric_cols + ["Date"])
    report_lines.append(f"Removed rows with {missing_before} missing value(s) in key columns.")

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    invalid_mask = (df["Quantity"] <= 0) | (df["Price"] <= 0) | (df["Total_Sales"] <= 0)
    invalid_count = invalid_mask.sum()
    df = df[~invalid_mask]
    report_lines.append(f"Removed {invalid_count} row(s) with invalid (zero/negative) values.")

    mismatch_mask = (df["Quantity"] * df["Price"] - df["Total_Sales"]).abs() > 1
    mismatch_count = mismatch_mask.sum()
    report_lines.append(
        f"Flagged {mismatch_count} row(s) where Total_Sales didn't match Quantity x Price "
        f"(kept, but worth a manual check)."
    )

    df = df.reset_index(drop=True)
    cleaned_count = len(df)

    print("\n--- Data Cleaning Summary ---")
    for line in report_lines:
        print(" -", line)
    print(f" -> {original_count} rows -> {cleaned_count} rows after cleaning\n")

    return df


# ---------------------------------------------------------------------------
# Step 3: Analyze data
# ---------------------------------------------------------------------------
def analyze_data(df: pd.DataFrame) -> dict:
    """Compute the core metrics used in the charts and the report."""
    results = {}

    results["total_sales"] = df["Total_Sales"].sum()
    results["total_units"] = df["Quantity"].sum()
    results["avg_order_value"] = df["Total_Sales"].mean()
    results["avg_unit_price"] = df["Price"].mean()
    results["num_orders"] = len(df)
    results["num_customers"] = df["Customer_ID"].nunique()

    results["sales_by_product"] = (
        df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    )
    results["units_by_product"] = (
        df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
    )

    df["Month"] = df["Date"].dt.to_period("M")
    results["monthly_sales"] = df.groupby("Month")["Total_Sales"].sum().sort_index()

    results["sales_by_region"] = (
        df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    )

    results["top_product"] = results["sales_by_product"].idxmax()
    results["top_region"] = results["sales_by_region"].idxmax()
    best_month = results["monthly_sales"].idxmax()
    results["best_month"] = str(best_month)
    results["best_month_value"] = results["monthly_sales"].max()

    return results


# ---------------------------------------------------------------------------
# Step 4: Visualize data
# ---------------------------------------------------------------------------
def make_bar_chart(results: dict):
    """Bar chart: total sales by product."""
    data = results["sales_by_product"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(data.index, data.values, color="#4C72B0")
    ax.set_title("Total Sales by Product", fontsize=14, fontweight="bold")
    ax.set_xlabel("Product")
    ax.set_ylabel("Total Sales ($)")
    ax.bar_label(bars, fmt="${:,.0f}".format, padding=3)
    plt.xticks(rotation=20)
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "sales_by_product.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def make_line_chart(results: dict):
    """Line chart: monthly sales trend."""
    data = results["monthly_sales"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data.index.astype(str), data.values, marker="o", color="#DD8452", linewidth=2)
    ax.set_title("Monthly Sales Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales ($)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "monthly_sales_trend.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def make_pie_chart(results: dict):
    """Pie chart: sales share by region."""
    data = results["sales_by_region"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52"],
    )
    ax.set_title("Sales Share by Region", fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "sales_share_by_region.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# Step 5: Report
# ---------------------------------------------------------------------------
def write_report(results: dict):
    lines = []
    lines.append("# E-commerce Sales Analysis — Report\n")
    lines.append("## Key Metrics\n")
    lines.append(f"- **Total Sales:** ${results['total_sales']:,.2f}")
    lines.append(f"- **Total Units Sold:** {results['total_units']:,}")
    lines.append(f"- **Number of Orders:** {results['num_orders']}")
    lines.append(f"- **Unique Customers:** {results['num_customers']}")
    lines.append(f"- **Average Order Value:** ${results['avg_order_value']:,.2f}")
    lines.append(f"- **Average Unit Price:** ${results['avg_unit_price']:,.2f}\n")

    lines.append("## Sales by Product\n")
    lines.append("| Product | Total Sales |")
    lines.append("|---|---|")
    for prod, val in results["sales_by_product"].items():
        lines.append(f"| {prod} | ${val:,.2f} |")
    lines.append("")

    lines.append("## Sales by Region\n")
    lines.append("| Region | Total Sales |")
    lines.append("|---|---|")
    for region, val in results["sales_by_region"].items():
        lines.append(f"| {region} | ${val:,.2f} |")
    lines.append("")

    lines.append("## Charts\n")
    lines.append("![Sales by Product](../visualizations/sales_by_product.png)\n")
    lines.append("![Monthly Sales Trend](../visualizations/monthly_sales_trend.png)\n")
    lines.append("![Sales Share by Region](../visualizations/sales_share_by_region.png)\n")

    lines.append("## Written Insights\n")
    lines.append(
        f"1. **{results['top_product']}** is the top-selling product by revenue, "
        f"generating ${results['sales_by_product'].max():,.2f} — the strongest "
        f"candidate for continued stock investment and promotion.\n"
    )
    lines.append(
        f"2. **{results['top_region']}** is the highest-revenue region, suggesting "
        f"demand (or marketing reach) is strongest there.\n"
    )
    lines.append(
        f"3. Sales peaked in **{results['best_month']}** at "
        f"${results['best_month_value']:,.2f}, which is worth cross-checking against "
        f"any promotions run that month. Note that the final month in the dataset is "
        f"partial (data ends mid-month), so its lower total reflects fewer days of "
        f"sales rather than a real decline.\n"
    )
    lines.append(
        f"4. The average order value across the dataset is ${results['avg_order_value']:,.2f} "
        f"from {results['num_orders']} orders across {results['num_customers']} unique "
        f"customers — tracking this over time is a good indicator of upsell/cross-sell "
        f"effectiveness.\n"
    )

    path = os.path.join(REPORT_DIR, "analysis_report.md")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS")
    print("=" * 60)

    df = load_data(DATA_PATH)
    df = clean_data(df)
    results = analyze_data(df)

    print("--- Key Metrics ---")
    print(f"Total Sales:        ${results['total_sales']:,.2f}")
    print(f"Total Units Sold:   {results['total_units']:,}")
    print(f"Number of Orders:   {results['num_orders']}")
    print(f"Unique Customers:   {results['num_customers']}")
    print(f"Avg Order Value:    ${results['avg_order_value']:,.2f}")
    print(f"Top Product:        {results['top_product']}")
    print(f"Top Region:         {results['top_region']}")
    print(f"Best Month:         {results['best_month']} (${results['best_month_value']:,.2f})")
    print()

    make_bar_chart(results)
    make_line_chart(results)
    make_pie_chart(results)
    write_report(results)

    print("\nDone! Check the visualizations/ and report/ folders.")


if __name__ == "__main__":
    main()
