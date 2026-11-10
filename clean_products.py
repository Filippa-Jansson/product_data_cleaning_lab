
import pandas as pd

EXTREME_PRICE_LIMIT = 10000   # flagged as possible luxury products
MAX_VALID_PRICE = 100000      # higher prices are treated as data errors

# Extract: read the raw product data
df = pd.read_csv("data/products_raw.csv", sep=";")

print("Raw data:")
print(df.head(10))
print("\nData info:")
df.info()

# Transform: clean text columns and convert prices to numbers
for column in ["id", "name", "currency"]:
    df[column] = df[column].str.strip()

# Values like "free" or "not_available" become NaN
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Flag possible problems
df["missing_currency"] = df["currency"].isna()
df["zero_price"] = df["price"] == 0
df["extreme_price"] = df["price"] > EXTREME_PRICE_LIMIT

print("\nFlagged products:")
print("Missing currency:", df["missing_currency"].sum())
print("Zero price:", df["zero_price"].sum())
print("Extreme price:", df["extreme_price"].sum())

# Reject impossible values
valid_products = df[
    (df["id"].notna()) &
    (df["name"].notna()) &
    (df["price"].notna()) &
    (df["price"] >= 0) &
    (df["currency"].notna()) &
    (df["price"] <= MAX_VALID_PRICE)
]

print("\nValid products:", len(valid_products))

# Load: save the cleaned data and a summary
valid_products.to_csv("output/valid_products.csv", index=False)

analytics_summary = pd.DataFrame({
    "average_price": [valid_products["price"].mean()],
    "median_price": [valid_products["price"].median()],
    "product_count": [len(valid_products)],
    "missing_price_count": [df["price"].isna().sum()],
})
analytics_summary.to_csv("output/analytics_summary.csv", index=False)

print("\nAnalytics summary:")
print(analytics_summary)

# Psycopg3 is a PostgreSQL adapter for Python. It is not used here, but in a full
# pipeline it could load the cleaned data into a PostgreSQL database (the "load" step in ETL).