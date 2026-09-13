# E-commerce Sales Analysis

**Week 4 Project — Data Visualization & First Complete Project**

## 1. Project Overview

This project is a complete, end-to-end data analysis pipeline built with Python,
pandas, and matplotlib. It analyzes 100 e-commerce sales records (`data/sales_data.csv`)
covering January–April 2024 to answer:

- Which product generates the most revenue?
- How do sales trend month over month?
- Which region contributes the largest share of sales?

**Goals**
- Practice the full analysis workflow: load → clean → analyze → visualize → report
- Produce at least two chart types (this project includes three: bar, line, pie)
- Turn raw numbers into written, actionable insights

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
4. Run the analysis:
   ```bash
   python main.py
   ```
5. Check the generated output:
   - `visualizations/` — the three PNG charts
   - `report/analysis_report.md` — the full written report

## 3. Code Structure

```
sales-analysis-project/
├── README.md                 # This file
├── main.py                   # Full pipeline: load, clean, analyze, visualize, report
├── requirements.txt          # Python dependencies
├── data/
│   └── sales_data.csv        # Raw dataset (100 rows x 7 columns)
├── visualizations/
│   ├── sales_by_product.png          # Bar chart
│   ├── monthly_sales_trend.png       # Line chart
│   └── sales_share_by_region.png     # Pie chart
└── report/
    └── analysis_report.md    # Metrics tables + written insights
```

`main.py` is organized into five clearly separated functions, one per pipeline stage:
`load_data()`, `clean_data()`, `analyze_data()`, the three `make_*_chart()` functions,
and `write_report()`. `main()` runs them in sequence and prints progress at each step.

## 4. Dataset

`data/sales_data.csv` has 100 rows and the following columns:

| Column | Description |
|---|---|
| Date | Date of the sale (2024-01-01 to 2024-04-09) |
| Product | One of: Phone, Laptop, Tablet, Headphones, Monitor |
| Quantity | Units sold in that order |
| Price | Unit price ($) |
| Customer_ID | Unique customer identifier |
| Region | One of: North, South, East, West |
| Total_Sales | Total revenue for that order ($) |

## 5. Technical Details

**Data pipeline**
- **Load:** `pandas.read_csv`, wrapped in `try/except` to fail gracefully on a missing,
  empty, or malformed file, and checked for required columns.
- **Clean:** parses dates, drops duplicate rows, drops rows with missing key values,
  drops rows with invalid (zero/negative) `Quantity`/`Price`/`Total_Sales`, and flags
  (without silently trusting) any row where `Total_Sales != Quantity * Price`. Every
  step is counted and printed so the cleaning is auditable, not silent. This dataset
  arrived clean, so most steps report 0 removed — they stay in place so the pipeline
  is robust against messier data too.
- **Analyze:** `groupby` aggregations for sales/units by product, by region, and by
  month (using `dt.to_period("M")` for calendar-month bucketing).
- **Visualize:** matplotlib `bar`, `plot` (line), and `pie` charts, each with titles,
  axis labels, and (for the bar chart) data labels for readability.
- **Report:** metrics and tables are written to a Markdown file that also embeds the
  three chart images, followed by four written insights derived from the numbers.

**Why these chart types:** a bar chart best compares totals across a small number of
discrete categories (products); a line chart is the standard way to show a trend over
time (monthly sales); a pie chart suits the region breakdown specifically because there
are only four regions and the question ("what share of sales comes from each region?")
is a part-of-a-whole question.

## 6. Testing Evidence

The pipeline includes defensive checks that were verified by testing against:
- A missing data file path → prints a clear error and exits instead of crashing
- An empty CSV → prints a clear error and exits
- A CSV missing a required column → prints a clear error and exits

The cleaning step's counters were also verified against a deliberately corrupted copy
of the dataset (duplicate row, missing values, negative quantity injected), confirming
each issue was correctly detected and removed before the real run below, which shows
the actual (clean) dataset passing through untouched:

```
--- Data Cleaning Summary ---
 - Removed 0 duplicate row(s).
 - Removed rows with 0 missing value(s) in key columns.
 - Removed 0 row(s) with invalid (zero/negative) values.
 - Flagged 0 row(s) where Total_Sales didn't match Quantity x Price (kept, but worth a manual check).
 -> 100 rows -> 100 rows after cleaning
```

## 7. Key Findings (see `report/analysis_report.md` for full detail)

- **Laptop** is the top-selling product by revenue ($3,889,210).
- **North** is the highest-revenue region (32.2% of total sales).
- Sales peaked in **March 2024** ($4,485,006); April is partial (data ends April 9),
  so its lower total is not a real decline.
- Average order value is $123,650 across 100 orders and 100 unique customers.

## 8. Visual Documentation

Screenshots of the three generated charts are in `visualizations/`:
`sales_by_product.png`, `monthly_sales_trend.png`, `sales_share_by_region.png`.
