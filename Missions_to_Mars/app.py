# import Flask
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# create an app, being sure to pass __name__
app = Flask(__name__)

# create flask_pymongo -> mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# index route


@app.route("/")
def index():
    db_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=db_info)

# scrape route


@app.route("/scrape")
def scraper():
    from scrape_mars import scrape

    info = scrape()

    mars_collection = mongo.db.mars_info
    mars_collection.drop()
    mars_collection.update({}, info, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
