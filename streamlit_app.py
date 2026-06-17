import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os


# Set page config for a cleaner layout
st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.title("Weather Around The World Dashboard")

st.title("🌐 Weather Around The World Dashboard")

st.markdown("""
This dashboard displays weather data collected through web scraping,
cleaned with Pandas, and stored in SQLite. Use the filters below to explore the data.
""")

# Connect to database securely
DB_FILE = "weather.db"

if not os.path.exists(DB_FILE):
    st.error(f"⚠️ Database file '{DB_FILE}' not found. Make sure it's pushed to your GitHub repository root folder!")
else:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM clean_weather", conn)
    conn.close()

    # --- USER INTERACTIONS (Sidebar Layout) ---
    st.sidebar.header("Filter Options")
    
    # 1. Multi-select dropdown for Cities (Default to all cities)
    all_cities = sorted(df["City"].unique())
    selected_cities = st.sidebar.multiselect(
        "Select Cities to Compare",
        options=all_cities,
        default=all_cities[:5] if len(all_cities) > 5 else all_cities # defaults to first 5 cities
    )

    # 2. Slider Filter (e.g., Temperature Range)
    min_temp = float(df["Temperature"].min())
    max_temp = float(df["Temperature"].max())
    selected_temp_range = st.sidebar.slider(
        "Select Temperature Range",
        min_value=min_temp,
        max_value=max_temp,
        value=(min_temp, max_temp)
    )

    # Apply the filters dynamically to the dataframe
    filtered_df = df[
        (df["City"].isin(selected_cities)) & 
        (df["Temperature"] >= selected_temp_range[0]) & 
        (df["Temperature"] <= selected_temp_range[1])
    ]

    # --- DASHBOARD LAYOUT & VISUALIZATIONS ---
    
    # Dataset Preview Section (Expandable to keep layout clean)
    with st.expander("🔍 View Raw Dataset Preview"):
        st.dataframe(filtered_df)


    # If the filters return empty data, handle it gracefully
    if filtered_df.empty:
        st.warning("No data matches the selected filters. Please adjust your selections in the sidebar.")
    else:
        # Layout components side-by-side using columns
        col1, col2 = st.columns(2)

        with col1:
            # Visualization 1: Dynamic Bar Chart
            st.subheader("📊 Temperature by City")
            fig1 = px.bar(
                filtered_df, # <-- Uses filtered data
                x="City",
                y="Temperature",
                color="City",
                title="Temperature Comparison"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Visualization 2: Dynamic Histogram
            st.subheader("🌡️ Temperature Distribution")
            fig2 = px.histogram(
                filtered_df, # <-- Uses filtered data
                x="Temperature",
                title="Overall Temperature Spread",
                nbins=10
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Visualization 3: Dynamic Scatter Plot (Takes full width below columns)
        st.subheader("📍 Temperature Scatter Plot")
        
        # If your scraper captured Humidity or Wind Speed, replacing 'Temperature' 
        # on the Y-axis would make this scatter plot even more insightful!
        y_axis_feature = "Temperature" 
        if "Humidity" in filtered_df.columns:
            y_axis_feature = "Humidity"
            
        fig3 = px.scatter(
            filtered_df, # <-- Uses filtered data
            x="City",
            y=y_axis_feature,
            color="City",
            size="Temperature" if y_axis_feature != "Temperature" else None,
            title=f"City vs {y_axis_feature} Plot"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Summary Statistics
        st.subheader("📋 Summary Statistics")
        st.write(filtered_df.describe(include="all"))
=======
# Visualization 3
st.subheader("Summary Statistics")

st.write(df.describe(include="all"))

