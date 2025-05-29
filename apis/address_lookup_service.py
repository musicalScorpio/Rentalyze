"""

author : Sam Mukherjee

"""
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import pydeck as pdk

# Load environment variables from .env file
load_dotenv('../env/relatize.env')
app = Flask(__name__)


OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")


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
            "town": components['town'],
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


if __name__ == '__main__':
    app.run(debug=True)
