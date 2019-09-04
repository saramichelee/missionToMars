# import necessary libraries
from flask import Flask, render_template, jsonify
import scrape_mars

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
# @app.route("/")
# def index():
#     mars_dictionary = {"current_weather": "Sol 265 (2019-08-25) low -99.4ºC (-146.9ºF) high -26.3ºC (-15.3ºF) winds from the SSE at 5.3 m/s (12.0 mph) gusting to 16.1 m/s (35.9 mph) pressure at 7.50 hPapic.twitter.com/9YLawm67zS",
#                          "featured_img": "https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA15283_ip.jpg"}
#     return render_template("index.html", dict=mars_dictionary)


@app.route("/scrape")
def scrape():

    return jsonify(scrape_mars.scrape())


if __name__ == "__main__":
    app.run(debug=True)