import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("Financials.csv")

# Remove leading/trailing whitespaces in column names and lowercase them
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Remove rows that are completely empty
df.dropna(how='all', inplace=True)

# Remove duplicates if any
df.drop_duplicates(inplace=True)

# Clean currency columns (remove $ and ,) and convert to float
currency_columns = ['units_sold', 'manufacturing_price', 'sale_price', 'gross_sales', 'discounts', 'sales', 'cogs', 'profit']

for col in currency_columns:
    if col in df.columns:
        df[col] = df[col].replace(r'[\$,]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Handle missing values
for col in df.columns:
    if df[col].dtype in [np.float64, np.int64]:
        df[col] = df[col].fillna(df[col].median())
    elif df[col].dtype == object:
        df[col] = df[col].fillna(df[col].mode()[0])

# Standardize text columns (remove extra spaces, lowercase)
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip().str.lower()

# Convert 'date' column to datetime and standardize format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.strftime('%d-%m-%Y')

# Check data types
print("Updated data types:\n", df.dtypes)

# Save cleaned dataset (optional)
df.to_csv("Financials_cleaned.csv", index=False)

# Preview cleaned data
print("\nCleaned Data Preview:")
print(df.head())
