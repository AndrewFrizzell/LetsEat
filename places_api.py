import os
import requests
import math

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
URL = "https://places.googleapis.com/v1/places:searchNearby"

def calculate_distance_miles(lat1, lon1, lat2, lon2):
    # Radius of Earth in miles
    earth_radius = 3958.8

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return round(earth_radius * c, 1)


def get_nearby_restaurants(latitude, longitude, radius=5000, max_results=20):
    if not API_KEY:
        raise ValueError("Missing GOOGLE_PLACES_API_KEY environment variable")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.primaryType,places.rating,places.priceLevel,places.formattedAddress,places.location"
    }

    body = {
        "includedTypes": ["restaurant"],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": float(radius)
            }
        }
    }

    response = requests.post(URL, headers=headers, json=body, timeout=15)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        return []

    data = response.json()
    places = data.get("places", [])

    price_map = {
        "PRICE_LEVEL_FREE": 0,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4,
    }

    restaurants = []

    for place in places:
        name = place.get("displayName", {}).get("text", "Unknown")
        cuisine = place.get("primaryType", "restaurant").replace("_", " ").title()
        rating = place.get("rating")
        address = place.get("formattedAddress", "Unknown")
        raw_price = place.get("priceLevel")
        price = price_map.get(raw_price, 2)

        place_location = place.get("location", {})
        place_lat = place_location.get("latitude")
        place_lon = place_location.get("longitude")

        if place_lat is not None and place_lon is not None:
            distance = calculate_distance_miles(latitude, longitude, place_lat, place_lon)
        else:
            distance = None

        restaurants.append({
            "name": name,
            "cuisine": cuisine,
            "price": price,
            "rating": rating,
            "distance": distance,
            "location": address
        })

    return restaurants