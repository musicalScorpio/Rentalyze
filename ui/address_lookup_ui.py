"""

author : Sam Mukherjee

"""
import pandas as pd
import streamlit as st
import requests
import pydeck as pdk
import folium
from streamlit_folium import st_folium
from folium import plugins


# Backend API endpoint (Flask API should be running on this endpoint)
API_URL = "http://127.0.0.1:5000/api"

def get_address_suggestions(query):
    """Fetch address suggestions from the backend API."""
    if query:
        response = requests.get(f"{API_URL}/address-suggestions?query={query}")
        if response.status_code == 200:
            return response.json()
    return []


def get_location_from_address(address):
    """Fetch latitude and longitude for the selected address."""
    url = f"{API_URL}/address-lookup?address={address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def main():
    st.title("Address Autocomplete with Leaflet Map")

    # Real-time text input to search address
    query = st.text_input("Enter an address", "")

    if len(query) >= 3:  # Trigger fetching only after 3 characters are typed
        # Fetch address suggestions from the Flask API
        suggestions = get_address_suggestions(query)

        # If suggestions are returned, show them in a dropdown
        if suggestions:
            address = st.selectbox("Choose an address", suggestions)
            if address:
                st.write(f"Selected Address: {address}")

                # Get the latitude and longitude of the selected address
                location = get_location_from_address(address)

                print('Location is ', location)
                if location:
                    latitude = location['latitude']
                    longitude = location['longitude']
                    # Define the Mapbox style (use your own Mapbox style if you have one)
                    #map_style = "mapbox://styles/mapbox/streets-v11"
                    # Create a folium map centered at the selected address
                    m = folium.Map(location=[latitude, longitude], zoom_start=15)

                    # Add a custom pin marker
                    folium.Marker(
                        location=[latitude, longitude],
                        popup=address,
                        icon=folium.Icon(icon='arrow-up', angle=180, color='blue')  # Custom pin icon
                    ).add_to(m)

                    # Display the map in Streamlit using st_folium
                    st_folium(m, width=700, height=500)
                else:
                    st.write("Location not found.")
        else:
            st.write("No suggestions found. Try again with more details.")
    else:
        st.write("Please type at least 3 characters to fetch suggestions.")


if __name__ == "__main__":
    main()

