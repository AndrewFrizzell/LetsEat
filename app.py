from flask import Flask, render_template, request
from places_api import get_nearby_restaurants, CUISINE_TYPE_MAP
import random

app = Flask(__name__)

@app.route("/")
def home():
    selected_cuisine = request.args.get("cuisine", "")
    max_price = request.args.get("price", "")
    min_rating = request.args.get("rating", "")
    max_distance = request.args.get("distance", "")
    pick_random = request.args.get("pick")

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:
        latitude = float(lat)
        longitude = float(lon)
    except (TypeError, ValueError):
        latitude = 29.5688
        longitude = -97.9647

    api_radius = 10000.0

    print("Selected cuisine:", selected_cuisine)
    print("selected cuisine: ", repr(selected_cuisine))

    restaurants = get_nearby_restaurants(
        latitude=latitude,
        longitude=longitude,
        radius=api_radius,
        max_results=20,
        cuisine=selected_cuisine
    )

    filtered_restaurants = restaurants
    
    #filter price
    if max_price:
        max_price = int(max_price)
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r["price"] <= max_price
        ]

    #min rating filter 
    if min_rating:
        min_rating = float(min_rating)
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r["rating"] >= min_rating
        ]

    #max distance filter
    if max_distance:
        max_distance = float(max_distance)
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r["distance"] <= max_distance
        ]

    cuisines = list(CUISINE_TYPE_MAP.keys())

    chosen_restaurant = None

    #random pick logic
    if pick_random and filtered_restaurants:
        chosen_restaurant = random.choice(filtered_restaurants)


    return render_template(
        "index.html",
         restaurants=filtered_restaurants,
         cuisines=cuisines,
         selected_cuisine=selected_cuisine,
         max_price=str(max_price) if max_price else "",
         min_rating=str(min_rating) if min_rating else "",
         max_distance=str(max_distance) if max_distance else "",
         chosen_restaurant=chosen_restaurant,
         lat=lat if lat else "",
         lon=lon if lon else ""
         )

if __name__ == "__main__":
    app.run(debug=True)