#%%

from flask import Flask, render_template, redirect, json
import pymongo
import os
import random
from pprint import pprint

#%%
print('Connecting to MongoDB')
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

list_dic = {
    'elon':lists['Elon'],
    'years':lists['Years'],
    'tweets':lists['Tweets'],
    'countries':lists['Countries'],
    'topTenCountries' : [],
    'topTenCorrelations' : [],

}

def renderer(chosen_variable):
    for feature in shapes['features']:
        feature['properties']['values'] = feature['properties'][chosen_variable]['values']
        feature['properties']['correlation'] = feature['properties'][chosen_variable]['correlation']
    topTen = sorted(shapes['features'], key = lambda x: float(x['properties']['correlation']))
    topTen = topTen[-10:]
    list_dic['topTenCountries'] = []
    list_dic['topTenCorrelations'] = []
    for i in range(10):
        list_dic['topTenCountries'].append(topTen[i]['properties']['ADMIN'])
        list_dic['topTenCorrelations'].append(topTen[i]['properties']['correlation'])
    list_dic['response_var'] = chosen_variable.capitalize()
    


#%%
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
            "values":feature["properties"]["happiness"]["values"],
            "correlation":feature["properties"]["happiness"]["correlation"],
            "happiness":feature["properties"]["happiness"],
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
    renderer('happiness')
    tweet = random.choice(list_dic['tweets'])
    return render_template("index.html", shapes = shapes, lists = list_dic, tweet = tweet)

@app.route("/happy")
def happy():
    renderer('happiness')
    tweet = random.choice(list_dic['tweets'])
    return render_template("index.html", shapes = shapes, lists = list_dic, tweet = tweet)

@app.route("/freedom")
def freedom():
    renderer('freedom')
    tweet = random.choice(list_dic['tweets'])
    return render_template("index.html", shapes = shapes, lists = list_dic, tweet = tweet)

@app.route("/GDP")
def GDP():
    renderer('GDP')
    tweet = random.choice(list_dic['tweets'])
    return render_template("index.html", shapes = shapes, lists = list_dic, tweet = tweet)

if __name__ == "__main__":
    app.run(debug=True)
