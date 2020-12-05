#%%
from flask import Flask, render_template, redirect
import pymongo
import os
from pprint import pprint
#%%
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MuskDB

#%%
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.Elon_db
elon_db = db.elon_db
lists = []
for i in elon_db.find({'Name':'Lists'}):
    lists.append(i)
lists = lists[0]

elon = lists["Elon"]
countries = lists["Countries"]
years = lists["Years"]

shapes = {
    "type": "FeatureCollection",
    "features": []
}
for feature in elon_db.find({'type':'Feature'}):
    new_entry = {
        "type":feature["type"],
        "properties":{
            "ADMIN":feature["properties"]["ADMIN"],
            "ISO_A3":feature["properties"]["ISO_A3"],
            "values":feature["properties"]["happy"]["values"],
            "correlation":feature["properties"]["happy"]["correlation"],
            "happy":feature["properties"]["happy"],
            "freedom":feature["properties"]["freedom"],
            "GDP":feature["properties"]["GDP"]
        },
        "geometry":feature["geometry"]
    }
    shapes["features"].append(new_entry)

#%%
app = Flask(__name__)
@app.route("/")
def musk():
    return render_template("index.html", shapes = shapes, elon = elon, years = years, countries = countries)
    
@app.route("/happy")
def happy():
    for feature in shapes['features']:
        feature['properties']['values'] = feature['properties']['happy']['values']
        feature['properties']['correlation'] = feature['properties']['happy']['correlation']
    return render_template("index.html", shapes = shapes, elon = elon, years = years, countries = countries)
@app.route("/freedom")
def freedom():
    for feature in shapes['features']:
        feature['properties']['values'] = feature['properties']['freedom']['values']
        feature['properties']['correlation'] = feature['properties']['freedom']['correlation']
    return render_template("index.html", shapes = shapes, elon = elon, years = years, countries = countries)
@app.route("/GDP")
def GDP():
    for feature in shapes['features']:
        feature['properties']['values'] = feature['properties']['GDP']['values']
        feature['properties']['correlation'] = feature['properties']['GDP']['correlation']
    return render_template("index.html", shapes = shapes, elon = elon, years = years, countries = countries)


if __name__ == "__main__":
    app.run(debug=True)
