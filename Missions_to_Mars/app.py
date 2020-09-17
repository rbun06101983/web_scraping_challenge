#importing the libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create instance of Flask App
app=Flask(__name__)

#use flask_pymongo to set up Mongo Connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

#Route to render index.html template using data from Mongo
@app.route("/")
def index():
    
    #find one record of data from the mongo database
    mars_dictionary=mongo.db.mars_dictionary.find_one()
    #Return Template and Data
    return render_template("index.html", mars=mars_dictionary)

@app.route("/scrape")
def scrape():

    mars_dictionary=mongo.db.mars_dictionary
    mars_data=scrape_mars.scrape()
    #Updating Mongo database using update and upsert
    mars_dictionary.update({}, mars_data, upsert=True)
    return redirect ('/', code=302)

if __name__ =="__main__":
    app.run(debug=True)