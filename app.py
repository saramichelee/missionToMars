# import necessary libraries
from flask import Flask, render_template
import scrape_mars

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/scrape")
def scrape():

    return scrape_mars.scrape()


if __name__ == "__main__":
    app.run(debug=True)