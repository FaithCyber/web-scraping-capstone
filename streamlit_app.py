import streamlit as st
import pandas as pd
import sqlite3

st.title("Weather Dashboard")

conn = sqlite3.connect("weather.db")
df = pd.read_sql_query(
    "SELECT * FROM clean_weather",
    conn
)
conn.close()

st.subheader("Weather Data")
st.dataframe(df)

city = st.selectbox(
    "Select a City",
    df["City"]
)

filtered = df[df["City"] == city]

st.subheader("Selected City")
st.dataframe(filtered)

# Chart 1
st.subheader("Temperature by City")
ax.bar(df["City"], df["Temperature"])
plt.xticks(rotation=45)
st.pyplot(fig)

# Chart 2
st.subheader("Temperature Distribution")
fig2, ax2 = plt.subplots()
ax2.hist(df["Temperature"])
st.pyplot(fig2)

# Chart 3
st.subheader("Summary Statistics")
st.write(df.describe())
