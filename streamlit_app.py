import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Chart 1 - Bar Chart
st.subheader("Temperature by City")

fig1 = px.bar(
    df,
    x="City",
    y="Temperature",
    title="Temperature by City"
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Histogram
st.subheader("Temperature Distribution")

fig2 = px.histogram(
    df,
    x="Temperature",
    title="Temperature Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Scatter Plot
st.subheader("Temperature Scatter Plot")

fig3 = px.scatter(
    df,
    x="City",
    y="Temperature",
    color="City",
    title="Temperature by City"
)

st.plotly_chart(fig3, use_container_width=True)

# Summary Statistics
st.subheader("Summary Statistics")
st.write(df.describe())