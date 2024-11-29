import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    # Load the reduced dataset with the average column
    #C:\Users\willi\School\cpts475\Geospatial-Analysis-of-Cancer\geospatial_cancer_data\geospatial_cancer_data\cancer_incidence\liver cancer\livercancer_inc_per100k_pop_2015_2019.csv
    data = pd.read_csv("..\geospatial_cancer_data\geospatial_cancer_data\cancer_incidence\liver cancer\livercancer_inc_per100k_pop_2015_2019.csv")
    data["Average Value"] = pd.to_numeric(data["Value"], errors="coerce")
    return data

# Load data
data = load_data()

# Streamlit UI
st.title("Geospatial Analysis Dashboard: Cancer Incidence")

# Filter options
st.sidebar.header("Filter Options")
view_option = st.sidebar.selectbox(
    "Select Value to Display",
    ["Value"]
)

# Display dataset preview
if st.sidebar.checkbox("Show Data Table"):
    st.subheader("Cancer Incidence Dataset")
    st.write(data)

# Plot map
st.subheader(f"Cancer Incidence by County: {view_option}")
fig = px.choropleth_mapbox(
    data.head(500),
    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
    locations="CountyFIPS",
    color=view_option,
    hover_name="County",
    hover_data={"State": True, "Value": True},
    color_continuous_scale=px.colors.sequential.Reds,
    range_color=(data[view_option].min(), data[view_option].max()),
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": 37.0902, "lon": -95.7129},  # Center on the U.S.
    title=f"Cancer Incidence by {view_option}"
)

st.plotly_chart(fig)

# Add conclusions or insights section
st.subheader("Insights and Notes")
st.write("""
- This dashboard visualizes cancer incidence rates by county.
- Use the sidebar to select which value to display on the map (Male, Female, or Average).
- The choropleth map highlights geographic disparities in cancer rates.
""")
