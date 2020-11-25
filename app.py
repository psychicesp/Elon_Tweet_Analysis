#%%
from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape, def_db
import os
#%%
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MarsDB
app = Flask(__name__)
def_db()

#%%
@app.route("/")
def mars():
    MARSdb = db.mars.find_one()
    return render_template('index.html', 
    news_title = MARSdb["News_Title"],
    news_desc = MARSdb["News_Desc"],
    img_url = MARSdb["Featured_Image"],
    table_html = MARSdb["Table"],
    Img_1_Title = MARSdb["Hemisphere_List"][0]['title'],
    Img_1_URL = MARSdb["Hemisphere_List"][0]['img_url'],
    Img_2_Title = MARSdb["Hemisphere_List"][1]['title'],
    Img_2_URL = MARSdb["Hemisphere_List"][1]['img_url'],
    Img_3_Title = MARSdb["Hemisphere_List"][2]['title'],
    Img_3_URL = MARSdb["Hemisphere_List"][2]['img_url'],
    Img_4_Title = MARSdb["Hemisphere_List"][3]['title'],
    Img_4_URL = MARSdb["Hemisphere_List"][3]['img_url']
    )


@app.route("/scrape")
def scraper():
    scrape()
    return redirect("/", code=302)
if __name__ == "__main__":
    app.run(debug=True)


# %%
