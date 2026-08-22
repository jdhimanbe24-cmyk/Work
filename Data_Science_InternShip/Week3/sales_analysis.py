import pandas as pd

# Load the sales dataset
df = pd.read_csv("sales_data.csv")

print("=" * 50)
print("SALES DATA ANALYSIS")
print("=" * 50)

# Basic exploration
print("\nDataset shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nData types:")
print(df.dtypes)

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Handle missing values
# Numeric missing values are filled with 0.
# Text/date missing values are filled with "Unknown".
numeric_columns = df.select_dtypes(include="number").columns
text_columns = df.select_dtypes(exclude="number").columns

df[numeric_columns] = df[numeric_columns].fillna(0)
df[text_columns] = df[text_columns].fillna("Unknown")

# Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
duplicates_removed = before - len(df)

# Calculate key metrics
total_revenue = df["Total_Sales"].sum()
total_quantity = df["Quantity"].sum()
average_sale = df["Total_Sales"].mean()
highest_sale = df["Total_Sales"].max()
lowest_sale = df["Total_Sales"].min()

# Product-level analysis
product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
product_quantity = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)

best_product_by_revenue = product_sales.idxmax()
best_product_revenue = product_sales.max()

best_product_by_quantity = product_quantity.idxmax()
best_product_quantity = product_quantity.max()

# Region-level analysis
region_sales = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
best_region = region_sales.idxmax()

# Print formatted report
print("\n" + "=" * 50)
print("KEY METRICS")
print("=" * 50)
print(f"Total Revenue       : ₹{total_revenue:,.2f}")
print(f"Total Quantity Sold : {total_quantity:,}")
print(f"Average Sale        : ₹{average_sale:,.2f}")
print(f"Highest Sale        : ₹{highest_sale:,.2f}")
print(f"Lowest Sale         : ₹{lowest_sale:,.2f}")
print(f"Duplicates Removed  : {duplicates_removed}")

print("\n" + "=" * 50)
print("BEST-SELLING PRODUCTS")
print("=" * 50)
print(f"By Revenue          : {best_product_by_revenue} (₹{best_product_revenue:,.2f})")
print(f"By Quantity         : {best_product_by_quantity} ({best_product_quantity:,} units)")

print("\n" + "=" * 50)
print("SALES BY PRODUCT")
print("=" * 50)
print(product_sales.to_string())

print("\n" + "=" * 50)
print("SALES BY REGION")
print("=" * 50)
print(region_sales.to_string())

print("\nAnalysis completed successfully.")
