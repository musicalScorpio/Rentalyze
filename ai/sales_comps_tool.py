"""

author : Sam Mukherjee

"""
import requests
import json


import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from pathlib import Path
import os

# Dynamically resolve path to relatize.env located in /env/ folder one level above this script
env_path = Path(__file__).resolve().parents[1] / "env" / "relatize.env"
load_dotenv(dotenv_path=env_path)

# Confirm it's loaded
ATTOM_BASE_URL_V1 = os.getenv("ATTOM_BASE_URL_V1")
ATTOM_BASE_URL_V2 = os.getenv("ATTOM_BASE_URL_V2")
ATTOM_API_KEY = os.getenv("ATTOM_API_KEY")
print("Loaded ENV Keys:")
print([k for k in os.environ.keys() if 'ATTOM' in k])

"""
def parse_sales_comparables(data, top_n=100):
    comps = sales_history = data['RESPONSE_GROUP']['RESPONSE']['RESPONSE_DATA']['PROPERTY_INFORMATION_RESPONSE_ext'][
            'SUBJECT_PROPERTY_ext']['PROPERTY']

    comparables =[]
    for comp in comps[1:top_n]:
        results = {}
        id = comp['COMPARABLE_PROPERTY_ext']['_IDENTIFICATION']['@RTPropertyID_ext']
        sales_history = comp['COMPARABLE_PROPERTY_ext']['SALES_HISTORY']
        sales_price = sales_history['@PropertySalesAmount']
        transaction_date = sales_history['@TransferDate_ext']
        street_address = comp['COMPARABLE_PROPERTY_ext']['@_StreetAddress']
        city= comp['COMPARABLE_PROPERTY_ext']['@_City']
        state = comp['COMPARABLE_PROPERTY_ext']['@_State']
        zipcode= comp['COMPARABLE_PROPERTY_ext']['@_PostalCode']
        lat = comp['COMPARABLE_PROPERTY_ext']['@LatitudeNumber']
        long = comp['COMPARABLE_PROPERTY_ext']['@LongitudeNumber']
        bath = comp['COMPARABLE_PROPERTY_ext']['STRUCTURE']['@TotalBathroomCount']
        bed = comp['COMPARABLE_PROPERTY_ext']['STRUCTURE']['@TotalBedroomCount']
        asser_market_value = comp['COMPARABLE_PROPERTY_ext']['_TAX']['@_AssessorMarketValue_ext']
        total_market_value = comp['COMPARABLE_PROPERTY_ext']['_TAX']['@_TotalAssessedValueAmount']

        owner_name = comp['COMPARABLE_PROPERTY_ext']['_OWNER']['@_Name']
        distance_from_subject= comp['COMPARABLE_PROPERTY_ext']['@DistanceFromSubjectPropertyMilesCount']

        results['id'] = id
        results['sales_price'] = sales_price
        results['transaction_date'] = transaction_date
        results['street_address'] = street_address
        results['city'] = city
        results['zipcode'] = zipcode
        results['lat'] = lat
        results['long'] = long
        results['bath'] = bath
        results['bed'] = bed
        results['asser_market_value'] = asser_market_value
        results['total_market_value'] = total_market_value
        results['owner_name'] = owner_name
        results['total_market_value'] = total_market_value
        results['distance_from_subject'] = distance_from_subject
        comparables.append(results)

    return comparables
"""


def get_sales_comparables_by_propertyid(address1,address2 , onlySales=True, onlydDetailed=False, api_key=ATTOM_API_KEY):
    property_id,bath_full,bed_full,heated_area = get_property_details(address1, address2, api_key)
    print(f'Got property id and it is {property_id}')

    base_url = f"{ATTOM_BASE_URL_V2}salescomparables/propid/"

    url = f"{base_url}{property_id}"
    query_params = {
        "searchType": "Radius",
        "minComps": 5,
        "maxComps": 7,
        "miles": 5,
        "sqFeetRange": heated_area,
        "bedroomsRange": bed_full,
        "bathroomRange": bath_full,
        "lotSizeRange": 2000,
        "saleDateRange": 6,
        "yearBuiltRange": 10,
        "ownerOccupied": "Both",
        "distressed": "IncludeDistressed"
    }
    headers = {
        "apikey": api_key,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=query_params)

    if response.status_code != 200:
        print(f"Error {response.status_code}:")
        print(response.text)
        raise Exception("API call failed with status code " + str(response.status_code))

    data = response.json()

    return parse_sales_comparables(data,onlySales,onlydDetailed)

def get_property_details(address1, address2, api_key=ATTOM_API_KEY):
    base_url = f"{ATTOM_BASE_URL_V1}basicprofile?address1={address1}&address2={address2}"
    print(f'Base url get_property_details is {base_url} ')
    url = base_url

    headers = {
        "apikey": api_key,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error {response.status_code}:")
        print(response.text)
        return None

    data = response.json()
    #print(json.dumps(data, indent=2))
    identifier = data['property'][0]['identifier']['Id']
    bath_full = data['property'][0]['building']['rooms']['bathsTotal']
    bed_full = data['property'][0]['building']['rooms']['beds']
    heated_area = data['property'][0]['building']['size']['livingSize']
    return identifier,bath_full,bed_full,heated_area

def parse_sales_comparables(data, onlySales=False, onlydDetailed=False, top_n=100):
    #TODO Do a check here
    if onlydDetailed:
            onlySales=False
    #print('DATA....')
    #print(data)
    comps = data['RESPONSE_GROUP']['RESPONSE']['RESPONSE_DATA']['PROPERTY_INFORMATION_RESPONSE_ext'][
        'SUBJECT_PROPERTY_ext']['PROPERTY']

    comparables = []

    for comp in comps[1:top_n]:
        try:
            comp_data = comp['COMPARABLE_PROPERTY_ext']

            results = {
                "id": comp_data['_IDENTIFICATION']['@RTPropertyID_ext'],
                "sales_price": comp_data['SALES_HISTORY']['@PropertySalesAmount'],
                "transaction_date": comp_data['SALES_HISTORY']['@TransferDate_ext'],
                "street_address": comp_data.get('@_StreetAddress', ''),
                "city": comp_data.get('@_City', ''),
                "state": comp_data.get('@_State', ''),
                "zipcode": comp_data.get('@_PostalCode', ''),
                "lat": comp_data.get('@LatitudeNumber', ''),
                "long": comp_data.get('@LongitudeNumber', ''),
                "bath": comp_data['STRUCTURE'].get('@TotalBathroomCount', ''),
                "bed": comp_data['STRUCTURE'].get('@TotalBedroomCount', ''),
                "asser_market_value": comp_data['_TAX'].get('@_AssessorMarketValue_ext', ''),
                "total_market_value": comp_data['_TAX'].get('@_TotalAssessedValueAmount', ''),
                "owner_name": comp_data['_OWNER'].get('@_Name', ''),
                "distance_from_subject": comp_data.get('@DistanceFromSubjectPropertyMilesCount', '')
            }

            comparables.append(results)

        except Exception as e:
            print(f"Skipping one comparable due to error: {e}")
            continue

    data_json = json.dumps({'comparables':comparables}, indent=2)

    if onlySales:
        return [float(item["sales_price"])
                for item in json.loads(data_json)['comparables']
                    if item["sales_price"]
                    and item["sales_price"].strip()
                    and float(item["sales_price"].strip()) > 0.0]
    if onlydDetailed:

        valid_tuples = [json.loads(data_json)
            (
                float(item["sales_price"].strip()),
                float(item["lat"]),
                float(item["long"]),
                item["street_address"],
                item["city"],
                item["state"],
                item["zipcode"],
                item["bed"],
                item["bath"],
                item["distance_from_subject"]
            )
            for item in json.loads(data_json)if item["sales_price"] and item["sales_price"].strip() and float(item["sales_price"].strip()) > 0.0

        ]
        return valid_tuples

    return data_json


def get_sales_comparables(street, city, county, state, zip_code,bedroomsRange=3,bathroomRange=2, api_key=ATTOM_API_KEY):
    base_url = "https://api.gateway.attomdata.com/property/v2/salescomparables/address"

    # Manually format the path just like the working curl (don't URL-encode slashes!)
    path = f"{street.replace(' ', '%20')}/{city}/{county}/{state}/{zip_code}"
    api_key =ATTOM_API_KEY
    #print(f'PATH !!!!! {path} AND api_key is {api_key}')

    query_params = {
        "searchType": "Radius",
        "minComps": 5,
        "maxComps": 7,
        "miles": 5,
        "bedroomsRange": bedroomsRange,
        "bathroomRange": bathroomRange,
        "sqFeetRange": 1000,
        "lotSizeRange": 2000,
        "saleDateRange": 6,
        "yearBuiltRange": 10,
        "ownerOccupied": "Both",
        "distressed": "IncludeDistressed"
    }

    url = f"{base_url}/{path}"

    headers = {
        "apikey": api_key,
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=query_params)

    if response.status_code != 200:
        #print(f"Error {response.status_code}:")
        #print(response.text)
        return None

    data = response.json()
    #print(json.dumps(data, indent=2))
    return data
