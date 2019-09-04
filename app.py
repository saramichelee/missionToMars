# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/m2mars_db")


# create route that renders index.html template
@app.route("/")
def index():
    information = mongo.db.mars_info.find()
    return render_template("index.html", info=information)


@app.route("/scrape")
def scraper():
    information = mongo.db.mars_info
    mars_data = scrape_mars.scrape()
    information.update({},mars_data, upsert=True)
    return redirect("/")

    # return jsonify(scrape_mars.scrape())

if __name__ == "__main__":
    app.run(debug=True)