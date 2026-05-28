import pandas as pd

# Load raw data
df = pd.read_csv("data/raw_data.csv")

print("BEFORE CLEANING:")
print(df.head())

# Remove duplicates
df = df.drop_duplicates()

# Remove empty rows
df = df.dropna(how="all")

# Optional: rename columns if needed
# df.columns = ["col1", "col2", "col3"]

print("AFTER CLEANING:")
print(df.head())

# Save cleaned data
df.to_csv("data/clean_data.csv", index=False)

print("Clean data saved!")