"""

author : Sam Mukherjee

"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium


import ai.sales_comps_tool as sales_comp_tool
import ai.charting_tool as charting_tool
import apis.rent_estimates_by_state_county_service as rent_estimates_by_state_county_service
import apis.address_lookup_service as address_lookup_service


def get_projected_rent(state_name, county_name):
    """Fetch address suggestions from the backend API."""
    if state_name and county_name:
        return rent_estimates_by_state_county_service.get_rental_data(state_name, county_name)
    return []


def get_address_suggestions(query):
    """Fetch address suggestions from the backend API."""
    if query:
        address_lookup_service.address_suggestions(query)
    return []


def get_location_from_address(address):
    return address_lookup_service.address_lookup(address)


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
                if location:
                    # After selecting the address and getting location
                    offer_price = st.number_input("Enter your offer price for the property ($)", min_value=0.0, step=1000.0)
                    rent_price = st.number_input("Enter rent($)", min_value=0.0,step=1000.0)
                    rent_data = get_projected_rent(state_name=location['state_code'], county_name=location['county'])

                    # Convert to DataFrame
                    rent_df = pd.DataFrame(rent_data)

                    # Display in Streamlit
                    st.subheader("🏠 Fair Market Rents by Unit Type")
                    st.dataframe(rent_df, use_container_width=True)
                    parts = [part.strip() for part in address.split(",")]
                    if offer_price and rent_price:
                        #url = f"{ADDRESS_LOOKUP_API_URL}/roi-estimate?price={offer_price}&rent={rent_price}&state={location['state_code']}&down_payment={.25 * offer_price}&credit_score={700}&has_mortgage=True"
                        #response = requests.get(url)
                        resp_json = address_lookup_service.roi_estimate(price=offer_price,rent=rent_price,state=location['state_code'],down_payment=.25 * offer_price,credit_score=700,has_mortgage=True)
                        if resp_json:
                            display_investment_summary(offer_price=offer_price, rent_price= rent_price, resp_json=resp_json)
                            st.write(f"Comparable sold recently")
                            print(f'Street is {parts[0]}')
                            data = sales_comp_tool.get_sales_comparables_by_propertyid(parts[0], location['state_code'])
                            fig = charting_tool.getChart(data,offer_price)
                            st.pyplot(fig)

                            #st.write(f"Assuming 700 credit..")
                            #st.write(f"You entered an offer of: ${offer_price:,.2f}")
                            #st.write(f"You rent for 12 months: ${rent_price * 12:,.2f}")
                            #st.write(f"Your P and I is : {resp_json['yearly_debt_service']}")
                            #st.write(f"Your Estimated Taxes is : {resp_json['estimated_property_tax']}")
                            #st.write(f"Your Estimated Insurance is : {resp_json['estimated_insurance']}")
                            #st.write(f"Your NOI is : {resp_json['noi']}")
                            #st.write(f"Your ROI is : {resp_json['roi_after_debt_service']}")

                    print('Location is ', location)
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

                    #Shows POI
                    # Let user select POI category
                    category = st.selectbox("Show nearby points of interest",
                                            ["recentsales", "grocery", "restaurant", "school", "hospital", "gym", "entertainment"])
                    # Icon color map for categories
                    icon_color = {
                        "grocery": "green",
                        "restaurant": "red",
                        "school": "purple",
                        "hospital": "darkred",
                        "gym": "orange",
                        "entertainment": "cadetblue",
                        "recentsales": "purple"
                    }.get(category, "gray")
                    print(f'category.title>>>>>>>>>> {str(category.title())}')
                    if str(category.title()).lower() != 'recentsales':
                        # Call the POI service
                        try:
                            response = requests.get("http://127.0.0.1:5002/nearby", params={
                                "lat": latitude,
                                "lon": longitude,
                                "category": category
                            })
                            response.raise_for_status()
                            poi_data = response.json().get("places", [])
                            # Add POIs to Folium map
                            add_to_map(category, icon_color, latitude, longitude, m, poi_data)
                        except Exception as e:
                            st.warning(f"Failed to fetch nearby {category}s: {e}")
                            poi_data = []
                    valid_tuples =None
                    try:
                        valid_tuples = sales_comp_tool.get_sales_comparables_by_propertyid(parts[0], location['state_code'], onlySales=False,onlydDetailed=True)
                    except Exception as e:
                        st.error(f"Failed to fetch nearby {category}s: {e}")

                    #Add Sales Comparable
                    poi_data_name_lat_long = [
                        {
                            #"name": f"${t[0]:,.0f} - {t[3]}, {t[4]}, {t[5]} {t[6]} ({t[7]}bd/{t[8]}ba)",
                            "price":t[0],
                            "name": t[3],
                            "lat": float(t[1]),
                            "lon": float(t[2])
                        }
                        for t in valid_tuples
                    ]

                    add_to_map(category, icon_color, latitude, longitude, m, poi_data_name_lat_long)

                    # Display the map in Streamlit using st_folium
                    st_folium(m, width=700, height=500)
                else:
                    st.write("Location not found.")
        else:
            st.write("No suggestions found. Try again with more details.")
    else:
        st.write("Please type at least 3 characters to fetch suggestions.")


def add_to_map(category, icon_color, latitude_of_source_property, longitude_of_source_property, m, poi_data_name_lat_long):
    # Add POI markers
    for poi in poi_data_name_lat_long:
        poi_name = poi.get("name", "Unnamed")
        poi_lat = poi["lat"]
        poi_lon = poi["lon"]
        poi_price = poi["price"]

        # Calculate distance in miles
        distance_miles = haversine_miles(latitude_of_source_property, longitude_of_source_property, poi_lat, poi_lon)
        popup_text = f"{category.title()}: {poi_name}<br>📍Sold for : {poi_price} <br> {distance_miles:.2f} miles away"

        folium.Marker(
            location=[poi_lat, poi_lon],
            popup=popup_text,
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(m)


from math import radians, sin, cos, sqrt, atan2

def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculate the distance between two lat/lon coordinates in miles."""
    R = 3958.8  # Earth radius in miles
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
def display_investment_summary(offer_price, rent_price, resp_json):
    """Display a nice-looking DataFrame with key investment metrics."""

    summary_data = {
        "Metric": [
            "Offer Price",
            "Down Payment",
            "Annual Rent",
            "Principal & Interest (Annual)",
            "Estimated Property Tax",
            "Estimated Insurance",
            "Cash-on-Cash",
            "Net Operating Income (NOI)",
            "ROI After Debt Service"
        ],
        "Value": [
            f"${offer_price:,.2f}",
            f"${resp_json['down_payment']:,.2f}",
            f"${rent_price * 12:,.2f}",
            f"${resp_json['yearly_debt_service']:,.2f}",
            f"${resp_json['estimated_property_tax']:,.2f}",
            f"${resp_json['estimated_insurance']:,.2f}",
            f"{resp_json['cash_on_cash']:.2f}%",
            f"${resp_json['noi']:,.2f}",
            f"{resp_json['roi_after_debt_service']:.2f}%"
        ]
    }

    st.subheader("📊 Property Investment Summary (Assuming 700 Credit Score)")
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)

if __name__ == "__main__":
    main()