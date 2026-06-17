import plotly.express as px
import plotly.data as pldata
import pandas as pd

# Load dataset
df = pldata.wind(return_type='pandas')

# Print first 10 rows
print("FIRST 10 ROWS")
print(df.head(10))

# Print last 10 rows
print("\nLAST 10 ROWS")
print(df.tail(10))

# Clean the strength column
df['strength'] = (
    df['strength']
    .str.replace(r'[^0-9.]', '', regex=True)
    .astype(float)
)

# Create interactive scatter plot
fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind Strength vs Frequency by Direction",
    labels={
        "strength": "Wind Strength",
        "frequency": "Frequency"
    }
)

# Save plot as HTML
fig.write_html("wind.html")

print("\nwind.html created successfully")