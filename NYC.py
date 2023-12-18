import streamlit as st
import pandas as pd
from PIL import Image
import folium
from streamlit_folium import folium_static


# Page Title
st.title("NYC Housing Rental Finder")
image = Image.open('airbnb.png')
st.image(image, use_column_width=False)

# Load Data
@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    df = pd.read_csv(url)
    return df

df = get_data()

# Display Initial Information
st.header('Welcome to NYC Housing Rental Finder!')
st.markdown("Explore available housing rentals in NYC. Select your preferences to find the perfect home.")
st.dataframe(df.head())

# Select Boroughs
boroughs = df['neighbourhood_group'].unique()
selected_borough = st.selectbox("Select a Borough", boroughs)

# Filter Neighborhoods based on Borough
neighborhoods = df[df['neighbourhood_group'] == selected_borough]['neighbourhood'].unique()
selected_neighborhoods = st.multiselect("Select Neighborhood(s)", neighborhoods)

# Set Price Range
price_range = st.slider("Set Price Range", float(df.price.min()), float(df.price.max()), (50., 300.))

# Filter Data based on Selections
filtered_df = df[(df['neighbourhood_group'] == selected_borough) & (df['neighbourhood'].isin(selected_neighborhoods)) & (df['price'].between(price_range[0], price_range[1]))]

# Display Results
st.subheader(f"Total {len(filtered_df)} housing rentals found in {', '.join(selected_neighborhoods)} {selected_borough} with prices between ${price_range[0]}  and  ${price_range[1]}")

# Create Folium Map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

# Add Markers to the Map
for index, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Name: {row['name']}\nNeighborhood: {row['neighbourhood']}\nHost name: {row['host_name']}\nRoom type: {row['room_type']}\nPrice: ${row['price']}",
    ).add_to(m)

# Display Folium Map in Streamlit
folium_static(m)

# Display Details on Marker Click
if st.checkbox("Show Details on Map Marker Click"):
    for index, row in filtered_df.iterrows():
        st.write(f"Name: {row['name']}")
        st.write(f"Neighborhood: {row['neighbourhood']}")
        st.write(f"Host name: {row['host_name']}")
        st.write(f"Room type: {row['room_type']}")
        st.write(f"Price: ${row['price']}")
        st.write("---")

# Save App State
state = st.experimental_get_query_params()
state['selected_borough'] = selected_borough
state['selected_neighborhoods'] = selected_neighborhoods
state['price_range'] = price_range
st.experimental_set_query_params(**state)
