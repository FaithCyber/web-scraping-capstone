import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

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

# City filter
city = st.selectbox(
    "Select a City",
    df["City"]
)

filtered = df[df["City"] == city]

st.subheader("Selected City")
st.dataframe(filtered)

# Visualization 1
st.subheader("Temperature by City")

fig1 = px.bar(
    df,
    x="City",
    y="Temperature",
    title="Temperature by City"
)

st.plotly_chart(fig1, use_container_width=True)

# Visualization 2
st.subheader("Temperature Distribution")

fig2 = px.histogram(
    df,
    x="Temperature",
    title="Temperature Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Visualization 3
st.subheader("Temperature Scatter Plot")

fig3 = px.scatter(
    df,
    x="City",
    y="Temperature",
    color="City",
    title="Temperature Scatter Plot"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Summary Statistics")
st.write(df.describe(include="all"))