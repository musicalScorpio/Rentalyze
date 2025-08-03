"""

author : Sam Mukherjee

"""
import json

from flask import Flask, request
import requests

from functools import lru_cache

app = Flask(__name__)

# Mapping of categories to Overpass API tags
CATEGORY_TAGS = {
    "grocery": '["shop"~"supermarket|grocery"]',
    "restaurant": '["amenity"="restaurant"]',
    "entertainment": '["amenity"~"cinema|theatre|arts_centre"]',
    "school": '["amenity"="school"]',
    "hospital": '["amenity"="hospital"]',
    "gym": '["leisure"="fitness_centre"]'
}

@app.route('/nearby', methods=['GET'])
def get_nearby_places_api():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    category = request.args.get('category')
    return get_nearby_place(lat=lat, lon=lon, category=category)
@lru_cache(maxsize=128)
def get_nearby_place (lat, lon,category):

    if not lat or not lon or not category:
        return json.dumps({"error": "Missing parameters: lat, lon, and category are required."})

    if category not in CATEGORY_TAGS:
        return json.dumps({"error": f"Unsupported category. Choose from: {list(CATEGORY_TAGS.keys())}"})

    overpass_tag = CATEGORY_TAGS[category]

    query = f'''
        [out:json];
        (
          node{overpass_tag}(around:15000, {lat}, {lon});

        );
        out body;
    '''

    try:
        response = requests.post("https://overpass-api.de/api/interpreter", data=query)
        response.raise_for_status()
        data = response.json()
        print(response.text)
        places = [
            {
                "name": el["tags"]["name"],
                "lat": el["lat"],
                "lon": el["lon"]
            }
            for el in data.get("elements", [])
        ]

        return json.dumps({"places": places})

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5002, debug=True)
