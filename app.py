#%%
from flask import Flask, render_template, redirect
import pymongo
import os
#%%
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MuskDB
app = Flask(__name__)

#%%
@app.route("/")
def musk():
    return "sup"
    
@app.route("/happy")
def happy():
   return "sup :)"


if __name__ == "__main__":
    app.run(debug=True)
