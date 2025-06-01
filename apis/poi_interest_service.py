"""

author : Sam Mukherjee

"""
from flask import Flask, request, jsonify
import requests

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
def get_nearby_places():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    category = request.args.get('category')

    if not lat or not lon or not category:
        return jsonify({"error": "Missing parameters: lat, lon, and category are required."}), 400

    if category not in CATEGORY_TAGS:
        return jsonify({"error": f"Unsupported category. Choose from: {list(CATEGORY_TAGS.keys())}"}), 400

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
                "name": el.get("tags", {}).get("name", "Unnamed"),
                "lat": el["lat"],
                "lon": el["lon"]
            }
            for el in data.get("elements", [])
        ]

        return jsonify({"places": places})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
