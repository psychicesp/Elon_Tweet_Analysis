#%%
from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape, def_db
import os
#%%
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MuskDB
app = Flask(__name__)
def_db()

#%%
@app.route("/")
def musk():
    return render_template("templates/index.html")
    
@app.route("/scrape")
def happy():


# %%
