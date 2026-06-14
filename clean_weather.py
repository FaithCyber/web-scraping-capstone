import pandas as pd

df = pd.read_csv("weather_data_raw.csv")

print("Before Cleaning")
print(df.info())

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

df["Temperature"] = df["Temperature"].astype(str)

print("\nAfter Cleaning")
print(df.info())

df.to_csv("weather_data_clean.csv", index=False)

print("Clean CSV saved.")