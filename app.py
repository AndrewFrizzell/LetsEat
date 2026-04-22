from flask import Flask, render_template, request
from restaurants import restaurants
import random

app = Flask(__name__)

@app.route("/")
def home():
    selected_cuisine = request.args.get("cuisine", "")
    max_price = request.args.get("price", "")
    min_rating = request.args.get("rating", "")
    pick_random = request.args.get("pick")

    filtered_restaurants = restaurants

    #Filterd cuisine
    if selected_cuisine:
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r["cuisine"] == selected_cuisine
        ]
    
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

    cusisines = sorted(set(r["cuisine"] for r in restaurants))

    chosen_restaurant = None

    #random pick logic
    if pick_random and filtered_restaurants:
        chosen_restaurant = random.choice(filtered_restaurants)


    return render_template(
        "index.html",
         restaurants=filtered_restaurants,
         cuisines=cusisines,
         selected_cuisine=selected_cuisine,
         max_price=str(max_price) if max_price else "",
         min_rating=str(min_rating) if min_rating else "",
         chosen_restaurant=chosen_restaurant
         )

if __name__ == "__main__":
    app.run(debug=True)