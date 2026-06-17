import streamlit as st
import pandas as pd
import sqlite3
import os

# Set page config for a cleaner, wide layout
st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.title("🌐 Weather Around The World Dashboard")

st.markdown("""
This dashboard displays weather data collected through web scraping,
cleaned with Pandas, and stored in SQLite. Use the sidebar filters below to explore the data.
""")

# Connect to database securely
DB_FILE = "weather.db"

if not os.path.exists(DB_FILE):
    st.error(f"⚠️ Database file '{DB_FILE}' not found. Make sure it's pushed to your GitHub repository root folder!")
else:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM clean_weather", conn)
    conn.close()

    # Clean up column names right away to prevent invisible spacing errors
    df.columns = df.columns.str.strip()
    
    # Track the correct column names dynamically (handles uppercase/lowercase variations)
    city_col = "City" if "City" in df.columns else ("city" if "city" in df.columns else df.columns[0])
    temp_col = "Temperature" if "Temperature" in df.columns else ("temperature" if "temperature" in df.columns else df.columns[1])

    # Ensure Temperature column is fully numeric for filtering and calculations
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df = df.dropna(subset=[temp_col])

    # --- USER INTERACTIONS (Sidebar Layout) ---
    st.sidebar.header("Filter Options")
    
    # 1. Dropdown/Multi-select filter for Cities
    all_cities = sorted(df[city_col].unique())
    selected_cities = st.sidebar.multiselect(
        "Select Cities to Compare",
        options=all_cities,
        default=all_cities[:5] if len(all_cities) > 5 else all_cities
    )

    # 2. Slider filter for Temperature Range
    min_temp = float(df[temp_col].min())
    max_temp = float(df[temp_col].max())
    selected_temp_range = st.sidebar.slider(
        "Select Temperature Range",
        min_value=min_temp,
        max_value=max_temp,
        value=(min_temp, max_temp)
    )

    # Apply filters dynamically
    filtered_df = df[
        (df[city_col].isin(selected_cities)) & 
        (df[temp_col] >= selected_temp_range[0]) & 
        (df[temp_col] <= selected_temp_range[1])
    ].copy()

    # --- DASHBOARD LAYOUT & VISUALIZATIONS ---
    
    # Dataset Preview Section (Expandable component)
    with st.expander("🔍 View Raw Dataset Preview"):
        st.dataframe(filtered_df, use_container_width=True)

    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your selections in the sidebar!")
    else:
        # Layout components side-by-side using columns
        col1, col2 = st.columns(2)

        with col1:
            # Visualization 1: Interactive Bar Chart
            st.subheader("📊 Temperature by City")
            # We set the index to City so the bar chart uses cities as labels
            chart1_data = filtered_df[[city_col, temp_col]].set_index(city_col)
            st.bar_chart(chart1_data, use_container_width=True)

        with col2:
            # Visualization 2: Temperature Distribution Trend
            st.subheader("🌡️ Temperature Trends")
            chart2_data = filtered_df[[city_col, temp_col]].set_index(city_col)
            st.line_chart(chart2_data, use_container_width=True)

        # Visualization 3: Area Map or Spread Plot (Takes full width below columns)
        st.subheader("📈 Overall Data Profile Plot")
        chart3_data = filtered_df[[temp_col]].copy()
        st.area_chart(chart3_data, use_container_width=True)

        # Summary Statistics
        st.subheader("📋 Summary Statistics")
        st.write(filtered_df.describe(include="all"))
     
