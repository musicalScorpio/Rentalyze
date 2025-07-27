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

load_dotenv('../env/relatize.env')

ATTOM_API_KEY = os.getenv("ATTOM_API_KEY")
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

    base_url = "https://api.gateway.attomdata.com/property/v2/salescomparables/propid/"

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
        return None

    data = response.json()

    return parse_sales_comparables(data,onlySales,onlydDetailed)

def get_property_details(address1, address2, api_key=ATTOM_API_KEY):
    base_url = f"https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/basicprofile?address1={address1}&address2={address2}"
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
    print('DATA....')
    print(data)
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
        valid_tuples = [
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
            for item in json.loads(data_json)
            if item.get("sales_price") and item["sales_price"].strip() and float(item["sales_price"].strip()) > 0.0
        ]
        return valid_tuples

    return data_json


def get_sales_comparables(street, city, county, state, zip_code,bedroomsRange=3,bathroomRange=2, api_key=ATTOM_API_KEY):
    base_url = "https://api.gateway.attomdata.com/property/v2/salescomparables/address"

    street = "34 Pine Course Loop"
    city = "Ocala"
    county = "Marion"
    state = "FL"
    zip_code = "34472"

    # Manually format the path just like the working curl (don't URL-encode slashes!)
    path = f"{street.replace(' ', '%20')}/{city}/{county}/{state}/{zip_code}"
    api_key ='1771dee1eb8a4add11504c4ae6240721'
    print(f'PATH !!!!! {path} AND api_key is {api_key}')

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
        print(f"Error {response.status_code}:")
        print(response.text)
        return None

    data = response.json()
    #print(json.dumps(data, indent=2))
    return data



"""
print(get_sales_comparables_by_propertyid('15592 SW 22nd Court Rd', 'Florida'))
print(get_property_id('34 Pine Course Loop', 'Florida'))
#Testing
street = "34 Pine Course Loop"
city = "Ocala"
#city = ""
county = "Marion"
state = "FL"
zip_code = "34472"

#get_sales_comparables(api_key, street, city, county, state, zip_code)

data = parse_sales_comparables(get_sales_comparables(street, city, county, state, zip_code,bedroomsRange=3,bathroomRange=2),onlySales=True)

print(data)
#sales_prices = [float(item["sales_price"]) for item in json.loads(data)['comparables']]
#print(sales_prices)
 
{
  "comparables": [
    {
      "id": "14934567",
      "sales_price": "220000.00",
      "transaction_date": "2025-05-02T00:00:00",
      "street_address": "8683 JUNIPER RD",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.095848",
      "long": "-82.063359",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "203021",
      "total_market_value": "164693",
      "owner_name": "YANDREY BAZAIN",
      "distance_from_subject": "0.5219648709"
    },
    {
      "id": "30754995",
      "sales_price": "113800.00",
      "transaction_date": "2025-02-13T00:00:00",
      "street_address": "14 JUNIPER TRACK DR",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.098627",
      "long": "-82.064241",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "211802",
      "total_market_value": "93505",
      "owner_name": "RAB20 LLC",
      "distance_from_subject": "0.57606937543"
    },
    {
      "id": "4396827",
      "sales_price": "245000.00",
      "transaction_date": "2025-06-02T00:00:00",
      "street_address": "53 JUNIPER TRAIL CIR",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.096683",
      "long": "-82.067954",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "186105",
      "total_market_value": "75199",
      "owner_name": "JESSI EVANS",
      "distance_from_subject": "0.79207523505"
    },
    {
      "id": "164220690",
      "sales_price": "240000.00",
      "transaction_date": "2025-03-27T00:00:00",
      "street_address": "5239 SE 92ND ST",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.087413",
      "long": "-82.06184",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "185392",
      "total_market_value": "179131",
      "owner_name": "JESSICA MARRA MARRA",
      "distance_from_subject": "0.79537668762"
    },
    {
      "id": "159504023",
      "sales_price": "232000.00",
      "transaction_date": "2025-01-16T00:00:00",
      "street_address": "1 LARCH RUN",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.107623",
      "long": "-82.06051",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "166650",
      "total_market_value": "166650",
      "owner_name": "LOPEZ MELENDEZ JATSIEL",
      "distance_from_subject": "0.7992362467"
    },
    {
      "id": "26361947",
      "sales_price": "269000.00",
      "transaction_date": "2025-05-28T00:00:00",
      "street_address": "79 JUNIPER TRAIL LOOP",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.098538",
      "long": "-82.068224",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "227529",
      "total_market_value": "106188",
      "owner_name": "79 JUNIPER TRAIL LOOP OCALA FL 3448",
      "distance_from_subject": "0.81318929609"
    },
    {
      "id": "12932265",
      "sales_price": "155000.00",
      "transaction_date": "2025-04-14T00:00:00",
      "street_address": "27 JUNIPER LOOP TER",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34480",
      "lat": "29.109111",
      "long": "-82.069641",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "146471",
      "total_market_value": "120997",
      "owner_name": "HUNTCO PROPERTIES LLC",
      "distance_from_subject": "1.21604228755"
    },
    {
      "id": "11360188",
      "sales_price": "0.00",
      "transaction_date": "2025-02-19T00:00:00",
      "street_address": "167 PINE CRSE",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34472",
      "lat": "29.116794",
      "long": "-82.043974",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "178470",
      "total_market_value": "178470",
      "owner_name": "167 PINE COURSE LLC",
      "distance_from_subject": "1.50662465684"
    },
    {
      "id": "209074141",
      "sales_price": "205000.00",
      "transaction_date": "2025-04-03T00:00:00",
      "street_address": "37 WILLOW RUN",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34472",
      "lat": "29.110434",
      "long": "-82.033609",
      "bath": "2.00",
      "bed": "2",
      "asser_market_value": "175658",
      "total_market_value": "158221",
      "owner_name": "HELMUT MANUEL MILLAN",
      "distance_from_subject": "1.57616732666"
    },
    {
      "id": "7996466",
      "sales_price": "290000.00",
      "transaction_date": "2025-05-21T00:00:00",
      "street_address": "15 DOGWOOD DR",
      "city": "OCALA",
      "state": "FL",
      "zipcode": "34472",
      "lat": "29.11997",
      "long": "-82.046632",
      "bath": "2.00",
      "bed": "3",
      "asser_market_value": "256913",
      "total_market_value": "194893",
      "owner_name": "KENNY R BISNATH",
      "distance_from_subject": "1.65177464944"
    }
  ]
} 

"""