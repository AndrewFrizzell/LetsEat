import os
import requests

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
URL = "https://places.googleapis.com/v1/places:searchNearby"

def get_nearby_restaurants(latitude, longitude, radius=5000, max_results=10):
    if not API_KEY:
        raise ValueError("Missing GOOGLE_PLACES_API_KEY environment variable")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName"
    }

    body = {
        "includedTypes": ["restaurant"],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 5000.0
            }
        }
    }

    response = requests.post(URL, headers=headers, json=body, timeout=15)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
    response.raise_for_status()

    data = response.json()
    places = data.get("places", [])

    restaurants = []
    for place in places:
        name = place.get("displayName", {}).get("text", "Unknown")
        restaurants.append({
            "name": name,
            "cuisine": "Unknown",
            "price": 2,
            "rating": None,
            "distance": None,
            "location": "Unknown"
        })

    return restaurants