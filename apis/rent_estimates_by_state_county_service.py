"""

author : Sam Mukherjee

"""
from flask import Flask, jsonify, request
import pandas as pd
import os
import utils.file_parser as fp
import base64
import rent_estimator_service
import utils.us_states as us_states

app = Flask(__name__)

# Load the data (this could be refactored for performance if it's large)
df = fp.parse_2025_data()
df = df.dropna(subset=["countyname", "stusps"])

# Helper function to get flag HTML
def get_flag_html(state_abbr):
    flag_path = f"../flags/{state_abbr.lower()}.png"
    if os.path.exists(flag_path):
        with open(flag_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"<img src='data:image/png;base64,{encoded}' width='20' style='margin-right: 8px;'>"
    return ""

# Helper function to get counties for a state
def get_counties_for_state(state_abbr):
    """Get all counties for a given state abbreviation."""
    counties = sorted(df[df["stusps"] == state_abbr]["countyname"].unique())
    return counties

@app.route('/api/rental-data', methods=['GET'])
def get_rental_data():
    state_name = request.args.get('state_name')
    county_name = request.args.get('county_name')

    # Convert state name to state abbreviation
    state_abbr =state_name # next((abbr for abbr, name in us_states.state_fullnames.items() if name == state_name), None)

    if state_abbr and county_name:
        # Filter the dataframe based on state and county
        rent_info = df[(df["stusps"] == state_abbr) & (df["countyname"] == county_name)]

        if not rent_info.empty:
            row = rent_info.iloc[0]
            rent_data = {
                "Unit Type": ["Studio", "1 Bedroom", "2 Bedroom", "3 Bedroom", "4 Bedroom"],
                "Rent ($)": [
                    f"${row['fmr_0']:,.0f}",
                    f"${row['fmr_1']:,.0f}",
                    f"${row['fmr_2']:,.0f}",
                    f"${row['fmr_3']:,.0f}",
                    f"${row['fmr_4']:,.0f}",
                ]
            }
            return jsonify(rent_data)
        else:
            return jsonify({"error": "No rent data available for the selected county."}), 404
    else:
        return jsonify({"error": "Invalid state or county selection."}), 400


@app.route('/api/counties', methods=['GET'])
def get_counties():
    """Fetch all counties for a given state."""
    state_name = request.args.get('state_name')

    # Convert state name to state abbreviation
    state_abbr = state_name #next((abbr for abbr, name in us_states.state_fullnames.items() if name == state_name), None)

    if state_abbr:
        counties = get_counties_for_state(state_abbr)
        return jsonify(counties)
    else:
        return jsonify({"error": "Invalid state selection."}), 400

@app.route('/api/rent', methods=['GET'])
def get_rentByZip():
    zip_code = request.args.get('zip_code')
    bedrooms = request.args.get('bedrooms')
    resp = rent_estimator_service.get_zip_rent(zip_code,bedrooms)
    return resp


if __name__ == '__main__':
    app.run(port=5001, debug=True)
