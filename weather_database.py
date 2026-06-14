import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("weather.db")

# Load CSV files
raw_df = pd.read_csv("weather_data_raw.csv")
clean_df = pd.read_csv("weather_data_clean.csv")

# Save DataFrames as tables
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

# Verify tables
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

print("Tables in database:")
for table in cursor.fetchall():
    print(table[0])

conn.close()

print("Database created successfully!")