from flask import Flask, render_template, request
from restaurants import restaurants

app = Flask(__name__)

@app.route("/")
def home():
    selected_cuisine = request.args.get("cuisine", "")

    if selected_cuisine:
        filtered_restaurants = [
            restaurant for restaurant in restaurants
            if restaurant["cuisine"] == selected_cuisine
        ]
    else:
        filtered_restaurants = restaurants

    cusisines = sorted(set(restaurant["cuisine"] for restaurant in restaurants))

    return render_template(
        "index.html",
         restaurants=filtered_restaurants,
         cuisines=cusisines,
         selected_cuisine=selected_cuisine
         )

if __name__ == "__main__":
    app.run(debug=True)