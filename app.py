from flask import Flask, render_template, request
from restaurants import restaurants
import random

app = Flask(__name__)

@app.route("/")
def home():
    selected_cuisine = request.args.get("cuisine", "")
    pick_random = request.args.get("pick")

    filtered_restaurants = restaurants

    #Filterd cuisine
    if selected_cuisine:
        filtered_restaurants = [
            r for r in filtered_restaurants
            if r["cuisine"] == selected_cuisine
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
         chosen_restaurant=chosen_restaurant
         )

if __name__ == "__main__":
    app.run(debug=True)