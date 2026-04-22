from flask import Flask, render_template
from restaurants import restaurants

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", restaurants=restaurants)

if __name__ == "__main__":
    app.run(debug=True)