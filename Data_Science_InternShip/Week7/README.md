# Customer Sales Analysis

**Week 5 Project — Advanced Data Manipulation with Pandas**

## 1. Project Overview

This project analyzes 100 sales transactions (`sales_data.csv`) alongside 500
customer relationship / churn records (`customer_data.csv`) to answer five
business questions:

1. Who are our most valuable customers?
2. What products sell best (and together)?
3. Which regions have the highest sales?
4. What are the seasonal trends?
5. How can we improve customer retention?

The goal is to practice pandas' more advanced toolkit — multi-condition
filtering, string operations, datetime feature extraction, merging, groupby
aggregations, and pivot tables — on a realistic two-table business scenario,
and to turn the results into an executive-ready report.

## 2. Setup Instructions

1. Clone or download this repository.
2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Open and run the notebook:
   ```bash
   jupyter notebook customer_analysis.ipynb
   ```
   The notebook already contains its own saved outputs (tables and charts),
   so you can also just read it top to bottom without re-running it.
5. To regenerate `analysis_report.pdf` from scratch, re-run the notebook first
   (so `visualizations/*.png` are refreshed), then run the PDF-building script
   included in this repo's history — or simply open the existing
   `analysis_report.pdf`, which already reflects the current data.

## 3. Code Structure

```
customer-sales-analysis/
├── README.md                    # This file
├── customer_analysis.ipynb      # Full analysis notebook (load → clean → merge →
│                                 #   analyze → visualize → insights), with saved output
├── sales_data.csv                # 100 sales transactions
├── customer_data.csv             # 500 customer relationship / churn records
├── analysis_report.pdf           # Executive report: metrics, charts, recommendations
├── requirements.txt              # Python dependencies
└── visualizations/
    ├── 01_sales_by_product.png
    ├── 02_monthly_sales_trend.png
    ├── 03_sales_share_by_region.png
    ├── 04_churn_rate_by_contract.png
    └── 05_order_value_vs_tenure.png
```

The notebook is organized to mirror the assignment's 7-day plan: data loading
& exploration, cleaning & preparation, customer analysis, sales pattern
analysis, advanced analysis (pivots + retention), the five-chart dashboard,
and a closing executive summary with recommendations.

## 4. Datasets

**sales_data.csv** (100 rows): `Date, Product, Quantity, Price, Customer_ID,
Region, Total_Sales`. Covers 2024-01-01 through 2024-04-09. Each of the 100
customer IDs (`CUST001`–`CUST100`) appears in exactly one order.

**customer_data.csv** (500 rows): `CustomerID, Tenure, MonthlyCharges,
TotalCharges, Contract, PaymentMethod, PaperlessBilling, SeniorCitizen,
Churn`. IDs are `C00001`–`C00500`. `Churn` is 1 if the customer has left, 0
if retained.

**Merging note:** the two files use different ID formats and were not built
with a shared key. To demonstrate a real merge, IDs are aligned by numeric
suffix extracted with a regex string operation (`CUST001` ↔ `C00001`, etc.),
linking each of the 100 sales orders to that customer's relationship record.
This is a documented assumption made for this exercise — not a verified
real-world identity match — and is called out again inside the notebook.

## 5. Technical Details

- **Datetime features:** `Date` is parsed to `datetime64`, then `Year`,
  `Month`, `Day`, `Weekday`, and a `YearMonth` period column are extracted for
  grouping and trend analysis.
- **String operations:** `.str.strip().str.title()` standardizes `Product`,
  `Region`, `Contract`, and `PaymentMethod`; `.str.extract(r'(\d+)')` pulls
  the numeric ID suffix used for merging.
- **Multi-condition filtering:** an AND filter (`Total_Sales >= 75th
  percentile & Churn == 1`) finds high-value churned customers; an OR filter
  (`Total_Sales >= 75th percentile | Tenure >= 55`) builds a broader
  "protect this relationship" list.
- **Merging:** an inner join on the aligned numeric customer ID combines
  order-level sales data with customer-level relationship data.
- **Aggregations (3+ types):** `groupby(...).agg(['sum', 'mean', 'count'])`
  is used for both regional and product-level summaries; `churn.mean()` is
  used as a churn-rate aggregation.
- **Pivot tables:** `pd.pivot_table` for Total Sales by Region × Product, and
  for Average Order Value by Region × Month; `pd.crosstab` for each region's
  product mix as a percentage share.
- **Visualization:** five matplotlib charts — bar, line, pie, bar, and a
  color-coded scatter plot — each with titles and axis labels, saved to
  `visualizations/` and embedded in both the notebook and the PDF report.
- **PDF report:** built with `reportlab` (Platypus), embedding the same
  charts plus metrics tables and the written insights.

## 6. Known Limitation: Cross-Selling

The assignment asks what products sell best together. In this dataset, each
of the 100 customers has exactly one recorded order, so there's no
repeat-purchase history to mine — a genuine market-basket / cross-sell
analysis isn't supportable without inventing purchases that aren't in the
data. The notebook and report are explicit about this and substitute a real,
supportable analysis instead: product mix by region.

## 7. Testing Evidence

Both files were checked for missing values and duplicate rows (`.isna().sum()`,
`.duplicated().sum()`) — none were found in either file. A calculated-column
check (`Quantity * Price` vs. `Total_Sales`) was run to catch data-entry
mismatches; none were found. The merge was verified by comparing row counts
before and after (`len(sales)` vs. `len(merged)`) to confirm no orders were
silently dropped or duplicated by the join. All 37 notebook cells run
top-to-bottom with zero errors — see the notebook's saved outputs.

## 8. Key Findings (full detail in `analysis_report.pdf`)

- **Top customer:** CUST016, $373,932 (Laptop).
- **Top product:** Laptop ($3.89M), ahead of Tablet and Phone.
- **Top region:** North ($3.98M), followed closely by South ($3.74M).
- **Seasonality:** sales rose to a March peak ($4.49M); the following month's
  lower total is a partial-month artifact (data ends April 9), not a decline.
- **Retention:** month-to-month contracts churn at 20.6% vs. 6.9% (two-year)
  and 4.3% (one-year) — the clearest lever for retention efforts.

## 9. Visual Documentation

All five dashboard charts are in `visualizations/` and are also embedded
directly in `customer_analysis.ipynb` and `analysis_report.pdf`.
