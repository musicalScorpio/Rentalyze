"""

author : Sam Mukherjee

"""
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import pandas as pd
import pydeck as pdk

# Load environment variables from .env file
load_dotenv('../env/relatize.env')
app = Flask(__name__)
df_roi = pd.read_csv("../data/state_tax_and_insurance_rates_all_50.csv")

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
import mortgage_estimator_service as mes

def parse_address_details(address):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&countrycode=us&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    result = response.json()
    print('Result from the Backend after address lookup is ', result)
    if response.status_code == 200 and result['results']:
        location = result['results'][0]['geometry']
        components = result['results'][0]['components']
        print('Location from the Backend is ', location)
        return location, components
    else:
        return None


@app.route('/api/address-lookup', methods=['GET'])
def address_lookup():
    address = request.args.get('address')

    if not address:
        return jsonify({"error": "Address is required"}), 400

    location, components = parse_address_details(address)

    if location:
        return jsonify({
            "latitude": location['lat'],
            "longitude": location['lng'],
            "county": components['county'],
            "zipcode": components['postcode'],
            "road": components['road'],
            "country": components['country'],
            "state": components['state'],
            "state_code": components['state_code'],
            "street_number": components['house_number']

        })
    else:
        return jsonify({"error": "Address not found or invalid"}), 404


def fetch_address_suggestions(query):
    # OpenCage API URL
    url = f'https://api.opencagedata.com/geocode/v1/json?q={query}&countrycode=us&key={OPENCAGE_API_KEY}&no_annotations=1'

    # Send GET request to OpenCage API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            print(data['results'])
            suggestions = [result['formatted'] for result in data['results']]
            return suggestions
        else:
            return []
    else:
        return None


@app.route('/api/address-suggestions', methods=['GET'])
def address_suggestions():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Fetch address suggestions from OpenCage
    suggestions = fetch_address_suggestions(query)

    if suggestions is not None:
        return jsonify(suggestions)
    else:
        return jsonify({"error": "Failed to fetch address suggestions"}), 500

@app.route('/api/roi-estimate', methods=['GET'])
def roi_estimate():
    try:
        price = float(request.args.get('price'))
        state = request.args.get('state', '').upper()
        rent = float(request.args.get('rent')) *12 #12 months rent
        down_payment = float(request.args.get('down_payment'))
        loan_amount = price - down_payment
        credit_score = float(request.args.get('credit_score'))
        has_mortgage = bool(request.args.get('has_mortgage'))
        yearly_debt_service = 0
        if has_mortgage:
            mortgage = mes.get_investor_mortgage_pi(credit_score=credit_score, loan_amount=loan_amount, years=30)
            yearly_debt_service = mortgage['monthly_payment']*12
        row = df_roi[df_roi['state'] == state]
        if row.empty:
            return None

        tax_rate = row.iloc[0]['tax_rate']
        insurance_rate = row.iloc[0]['insurance_rate']

        property_tax = round(price * tax_rate, 2)
        insurance = round(price * insurance_rate, 2)
        noi = (rent - property_tax - insurance - yearly_debt_service)
        cash_on_cash = noi /down_payment * 100
        roi_after_debt_service = noi / price * 100

        return jsonify({
            "state": state,
            "home_price": price,
            "estimated_property_tax": property_tax,
            "estimated_insurance": insurance,
            "property_tax_rate": tax_rate,
            "down_payment": down_payment,
            "yearly_debt_service": yearly_debt_service,
            "insurance_rate": insurance_rate,
            "noi": noi,
            "cash_on_cash": cash_on_cash,
            "roi_after_debt_service": roi_after_debt_service
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(debug=True)
