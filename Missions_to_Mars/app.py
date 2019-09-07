# -*- coding: utf-8 -*-
"""
Created 2019
Author: GB
"""

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars_dict=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars=mongo.db.mars_data
    # Run the scrape function
    #mars_data=scrape_mars.scrape_all()
    mars_data=mars.scrape_all()
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

    # Run the scrape function
    #scrape_mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    #mongo.db.collection.update({}, scrape_mars_data, upsert=True)

    # Redirect back to home page
    #return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)