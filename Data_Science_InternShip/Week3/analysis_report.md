# Sales Data Analysis Report

## 1. Project Overview

This project analyzes a 100-row sales dataset using Python and pandas. The goal is to clean the data, calculate important sales metrics, identify the best-selling products, and summarize the results in a clear report.

## 2. Dataset

- Rows: 100
- Columns: 7
- Main columns: Date, Product, Quantity, Price, Customer_ID, Region, Total_Sales
- Date values were not supplied as actual dates in the provided dataset, so the Date column is retained as `Not provided`.

## 3. Setup Instructions

1. Install Python 3.
2. Open a terminal in this project folder.
3. Install the required library:

```bash
pip install -r requirements.txt
```

4. Run the analysis:

```bash
python sales_analysis.py
```

## 4. Analysis Steps

1. Loaded the CSV file using `pandas.read_csv()`.
2. Checked the dataset shape, columns, and data types.
3. Checked all columns for missing values.
4. Filled missing numeric values with `0` and missing text values with `Unknown`.
5. Removed duplicate rows.
6. Calculated total revenue, total quantity, average sale, highest sale, and lowest sale.
7. Grouped sales by product and region.
8. Identified the best-selling product by revenue and quantity.

## 5. Key Findings

| Metric | Result |
|---|---:|
| Total Revenue | ₹12,365,048.00 |
| Total Quantity Sold | 478 |
| Average Sale | ₹123,650.48 |
| Highest Sale | ₹373,932.00 |
| Lowest Sale | ₹6,540.00 |

### Best-selling products

- **By revenue:** Laptop — ₹3,889,210.00
- **By quantity:** Laptop — 136 units

### Sales by product

Product
Laptop        3889210
Tablet        2884340
Phone         2859394
Headphones    1384033
Monitor       1348071

### Sales by region

Region
North    3983635
South    3737852
East     2519639
West     2123922

## 6. Technical Details

The project uses pandas DataFrames for tabular data processing. `groupby()` is used for product and region summaries, while aggregation functions such as `sum()`, `mean()`, `max()`, and `min()` calculate the required metrics.

## 7. Testing Evidence

The program validates the dataset by:

- Printing the number of rows and columns.
- Printing column names and data types.
- Checking missing values.
- Removing duplicate rows.
- Calculating multiple independent sales metrics.
- Printing product and regional summaries.

## 8. Conclusion

The analysis successfully demonstrates basic real-world data analysis with pandas. It cleans the provided dataset, calculates key business metrics, and identifies the strongest products and regions by sales.
