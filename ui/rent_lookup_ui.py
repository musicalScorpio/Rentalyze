import streamlit as st
import requests
import pandas as pd

# API URL
RENTAL_API_URL = "http://127.0.0.1:5000/api/rental-data"
COUNTY_API_URL = "http://127.0.0.1:5000/api/counties"
state_colors = {
        "CA": "#0039A6",   # California - Blue
        "FL": "#FF8C00",   # Florida - Orange
        "TX": "#BF0A30",   # Texas - Red
        "NY": "#002868",   # New York - Navy Blue
        "GA": "#B22234",   # Georgia - Red
        "AZ": "#EDC92E",   # Arizona - Yellow/Gold
        "IL": "#1464B4",   # Illinois - Blue
        "NC": "#004684",   # North Carolina - Dark Blue
        "WA": "#006400",   # Washington - Forest Green
        "MA": "#004C99",   # Massachusetts - Navy
        # Add more as needed...
}

state_abbr_to_name = {
    "AL": "alabama",
    "AK": "alaska",
    "AZ": "arizona",
    "AR": "arkansas",
    "CA": "california",
    "CO": "colorado",
    "CT": "connecticut",
    "DE": "delaware",
    "FL": "florida",
    "GA": "georgia",
    "HI": "hawaii",
    "ID": "idaho",
    "IL": "illinois",
    "IN": "indiana",
    "IA": "iowa",
    "KS": "kansas",
    "KY": "kentucky",
    "LA": "louisiana",
    "ME": "maine",
    "MD": "maryland",
    "MA": "massachusetts",
    "MI": "michigan",
    "MN": "minnesota",
    "MS": "mississippi",
    "MO": "missouri",
    "MT": "montana",
    "NE": "nebraska",
    "NV": "nevada",
    "NH": "new_hampshire",
    "NJ": "new_jersey",
    "NM": "new_mexico",
    "NY": "new_york",
    "NC": "north_carolina",
    "ND": "north_dakota",
    "OH": "ohio",
    "OK": "oklahoma",
    "OR": "oregon",
    "PA": "pennsylvania",
    "RI": "rhode_island",
    "SC": "south_carolina",
    "SD": "south_dakota",
    "TN": "tennessee",
    "TX": "texas",
    "UT": "utah",
    "VT": "vermont",
    "VA": "virginia",
    "WA": "washington",
    "WV": "west_virginia",
    "WI": "wisconsin",
    "WY": "wyoming"
}

state_fullnames = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "AS": "American Samoa",
    "GU": "Guam",
    "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico",
    "VI": "U.S. Virgin Islands",
    "DC": "District of Columbia"
}
def get_counties_for_state(state_name):
    """Get counties for a given state from the Flask API."""
    response = requests.get(f"{COUNTY_API_URL}?state_name={state_name}")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_rental_data(state_name, county_name):
    """Get rental data for a given state and county."""
    response = requests.get(f"{RENTAL_API_URL}?state_name={state_name}&county_name={county_name}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# --- Setup ---
st.set_page_config(page_title="Rentalyze", layout="centered")

# Load CSS
def load_css(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("../styles/brand_animate.css")

# Logo (Rentalyze Text Only with Animation)
st.markdown("""
    <div class="brand-wrapper">
        <div class="brand-text">
            <span>R</span><span>e</span><span>n</span><span>t</span><span>a</span><span>l</span><span>y</span><span>z</span><span>e</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("Find HUD-published rental estimates by county and bedroom type (FY 2025).")

# --- State Selection ---
states = ["-- Select a state --"] + [state_fullnames[s] for s in state_fullnames]
selected_name = st.selectbox("🔽 Select State", states)
state = None

if selected_name != "-- Select a state --":
    # Find the key in the dictionary that matches the selected value
    state = next((abbr for abbr, name in state_fullnames.items() if name == selected_name), None)

# --- County + Flag Display ---
if state:
    # Fetch all counties for the selected state
    counties = get_counties_for_state(state)

    if counties:
        county = st.selectbox("📍 Select County", ["-- Select a county --"] + counties)

        if county != "-- Select a county --":
            # Get rental data for the selected county
            rent_data = get_rental_data(state, county)

            if rent_data:
                rent_df = pd.DataFrame(rent_data)
                st.table(rent_df)

                st.info("These rents represent HUD's estimates of what renters typically pay, including utilities.")
            else:
                st.warning("No rental data available for the selected county.")
    else:
        st.warning("No counties found for the selected state.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ by Rentalyze | HUD FMR FY2025 Data")