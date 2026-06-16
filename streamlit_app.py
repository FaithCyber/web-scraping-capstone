import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.title("Weather Around The World Dashboard")

st.write("""
This dashboard displays weather data collected through web scraping,
cleaned with Pandas, and stored in SQLite.
""")

# Connect to database
conn = sqlite3.connect("weather.db")

df = pd.read_sql_query(
    "SELECT * FROM clean_weather",
    conn
)

conn.close()

st.subheader("Dataset Preview")
st.dataframe(df)

# Sidebar filter
city_column = df.columns[0]

selected_city = st.sidebar.selectbox(
    "Select a City",
    ["All"] + list(df[city_column].unique())
)

if selected_city != "All":
    df = df[df[city_column] == selected_city]

# Visualization 1
st.subheader("Record Count")

fig1, ax1 = plt.subplots()

df.groupby(city_column).size().plot(
    kind="bar",
    ax=ax1
)

st.pyplot(fig1)

# Visualization 2
st.subheader("Data Distribution")

numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) > 0:
    selected_numeric = st.selectbox(
        "Choose Numeric Column",
        numeric_cols
    )

    fig2, ax2 = plt.subplots()

    df[selected_numeric].hist(ax=ax2)

    st.pyplot(fig2)

# Visualization 3
st.subheader("Summary Statistics")

st.write(df.describe(include="all"))
