import pandas as pd
import sqlite3

# Load CSV files
raw_df = pd.read_csv("weather_data_raw.csv")
clean_df = pd.read_csv("weather_data_clean.csv")

print("RAW DATA")
print(raw_df.head())
print(f"Rows: {len(raw_df)}")

print("\nCLEAN DATA")
print(clean_df.head())
print(f"Rows: {len(clean_df)}")

# Connect to SQLite database
conn = sqlite3.connect("weather.db")

# Save each dataframe to its own table
raw_df.to_sql(
    "raw_weather",
    conn,
    if_exists="replace",
    index=False
)

clean_df.to_sql(
    "clean_weather",
    conn,
    if_exists="replace",
    index=False
)

# Verify tables exist
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

print("\nTABLES IN DATABASE:")
for table in cursor.fetchall():
    print(table[0])

conn.close()

print("\nDatabase created successfully!")