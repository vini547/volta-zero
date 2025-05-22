import folium
from streamlit_folium import st_folium

# Create a Folium map object centered at the given location
m = folium.Map(location=[-11.93554, -61.99982], zoom_start=13)

# Add a marker at the specified location with a popup message
folium.Marker(
    location=[-11.93554, -61.99982],
    popup="Marker Location: -11.93554, -61.99982",
    tooltip="Click for more info"
).add_to(m)

# Render the map in Streamlit with custom dimensions
st_data = st_folium(m, width=300, height=300)
