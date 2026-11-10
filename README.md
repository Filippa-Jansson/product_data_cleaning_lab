# Product Data Cleaning

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)

A small ETL pipeline in Python that cleans messy product data, flags possible problems, rejects impossible values and produces a summary. Built as part of the Data Platform course in the Data Engineering program at STI.

## The data

`data/products_raw.csv` contains 55 products with typical data quality issues:

- Missing ids, names, prices and currencies
- Extra spaces, like `" shoes "` and `" SEK "`
- Prices that are text (`free`, `not_available`), negative or zero
- A placeholder price of 999,999
- Mixed date formats

## Pipeline

**Extract:** reads the raw CSV file with pandas.

**Transform:**
- Removes extra spaces from text columns
- Converts prices to numbers, so text values become missing
- Flags products with missing currency, a price of zero or a price above 10,000 (possible luxury products)
- Rejects products with a missing id, name, price or currency, a negative price, or a price above 100,000

**Load:** saves the valid products and a summary to `output/`.

## Results

| Metric | Value |
|---|---|
| Valid products | 44 of 55 |
| Average price | 1,784 SEK |
| Median price | 600 SEK |
| Products with missing price | 5 |

The coat priced at 999,999 is rejected as a data error. With it, the average price would have been about 24,000 SEK, far from the median. Expensive but realistic products, like a watch for 15,000 SEK, are flagged but kept.

## Project structure

```
├── data/
│   └── products_raw.csv         # raw input
├── output/
│   ├── valid_products.csv       # cleaned products with flags
│   └── analytics_summary.csv    # summary statistics
└── clean_products.py            # the pipeline
```


## Possible improvements

- Save rejected products to their own file
- Standardize the date formats
- Load the cleaned data into PostgreSQL with Psycopg3