import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# Set page config for a cleaner layout
st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.title("🌐 Weather Around The World Dashboard")

# Connect to database securely
DB_FILE = "weather.db"

if not os.path.exists(DB_FILE):
    st.error(f"⚠️ Database file '{DB_FILE}' not found. Make sure it's pushed to your GitHub repository root folder!")
else:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM clean_weather", conn)
    conn.close()

    # --- DEBUGGING SECTION ---
    # This will print out exactly what columns Pandas sees in your database
    st.write("### 🔍 Database Column Debugging")
    st.write("Your actual database columns are:", list(df.columns))
    
    # Let's clean column names by stripping any hidden spaces and matching capitalization
    # This automatically forces columns to match what our script expects if it's just a spacing issue
    df.columns = df.columns.str.strip()
    
    # --- AUTOMATIC COLUMN DETECTION ---
    # This checks if your database uses lower-case names and adjusts them dynamically
    city_col = "City" if "City" in df.columns else ("city" if "city" in df.columns else df.columns[0])
    temp_col = "Temperature" if "Temperature" in df.columns else ("temperature" if "temperature" in df.columns else df.columns[1])

    st.write(f"Using column **'{city_col}'** for Cities and **'{temp_col}'** for Temperature.")

    # --- USER INTERACTIONS (Sidebar Layout) ---
    st.sidebar.header("Filter Options")
    
    all_cities = sorted(df[city_col].unique())
    selected_cities = st.sidebar.multiselect(
        "Select Cities to Compare",
        options=all_cities,
        default=all_cities[:5] if len(all_cities) > 5 else all_cities
    )

    min_temp = float(df[temp_col].min())
    max_temp = float(df[temp_col].max())
    selected_temp_range = st.sidebar.slider(
        "Select Temperature Range",
        min_value=min_temp,
        max_value=max_temp,
        value=(min_temp, max_temp)
    )

    # Apply the filters  using our detected column names
    filtered_df = df[
        (df[city_col].isin(selected_cities)) & 
        (df[temp_col] >= selected_temp_range[0]) & 
        (df[temp_col] <= selected_temp_range[1])
    ]

    # -DASHBOARD LAYOUT VISUALIZATIONS 
    with st.expander("🔍 View Raw Dataset Preview"):
        st.dataframe(filtered_df)

    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your selections in the sidebar!")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Temperature by City")
            fig1 = px.bar(
                filtered_df, 
                x=city_col,      
                y=temp_col,      
                color=city_col,  
                title="Temperature Comparison"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader("🌡️ Temperature Distribution")
            fig2 = px.histogram(
                filtered_df, 
                x=temp_col,      # <-- Dynamic Column Name
                title="Overall Temperature Spread",
                nbins=10
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📍 Temperature Scatter Plot")
        fig3 = px.scatter(
            filtered_df, 
            x=city_col,          
            y=temp_col,     
            color=city_col,     
            title="City vs Temperature Plot"
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("📋 Summary Statistics")
        st.write(filtered_df.describe(include="all"))

