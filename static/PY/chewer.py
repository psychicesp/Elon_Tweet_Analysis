#%%
#imports
print('====Getting Imports====')
import pandas as pd
import json
import os
from scipy import stats as st
from pprint import pprint
import pymongo
print('***CHOMP***')
#%%
###Connecting to Mongo###
print("====Connecting to MongoDB====")
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.Elon_db
elon_db = db.elon_db
print('***CHOMP***')
#%%
print("====Opening Files====")

filepath = os.path.join("..","Data","countries.geojson")

with open(filepath) as jsonfile:
    shapes_json = json.load(jsonfile)
filepath = os.path.join("..","Data","countries-land-10km.geo.json")

with open(filepath) as jsonfile:
    small_shapes_json = json.load(jsonfile)

elon = pd.read_csv("../Data/elonmusk.csv")

#To get the individual tweets
tweets = elon['tweet'].tolist()
print('***CHOMP***')
# %%
print('====Getting Lists====')
elon.head()
def year_getter(x):
    try:
        x = x.split('-')
        x = x[0]
    except:
        pass
    return x

elon['year'] = elon['date'].apply(year_getter)

output_dict = {}

elon_year = elon.groupby('year').agg({
    'conversation_id': 'count'
})
elon_year = elon_year.reset_index()

### 'Elon' carries the list of elon tweet numbers ###
Elon = elon_year['conversation_id'].tolist()

# %%
###'years' carries the list of years###
years = [2015,2016,2017,2018,2019,2020]
print('***CHOMP***')
print('====Parsing csvs====')

#To convert all fles into CSVs
happyDFs = []
file_structure = '../Data/Happiness/'
for i in years:
    happyDFs.append(pd.read_csv(f"{file_structure}{str(i)}.csv"))
countries = happyDFs[0]['Country'].tolist()

#The following dictionaries to extract data to
Happy = {}
GDP = {}
Freedom = {}
#%%
#2020 GDP values are in a higher order of magnitude, it seems, so I'm dividing them all by 10.
happyDFs[-1]['Economy (GDP per Capita)'] = happyDFs[-1]['Economy (GDP per Capita)']/10
#%%

###'countries' carries the list of countries; the following code filters out any country that is not common to every .csv ###
for df in happyDFs:
    for country in countries:
        df_countries = df['Country'].tolist()
        if country not in df_countries:
            countries.remove(country)

#Making sure all necessary dictionary keys exist:
for country in countries:
    Happy[country] = {}
    Happy[country]['Values'] = []
    Happy[country]['Correlation'] = 0
    Freedom[country] = {}
    Freedom[country]['Values']= []
    Freedom[country]['Correlation'] = 0
    GDP[country] = {}
    GDP[country]['Values'] = []
    Freedom[country]['Correlation'] = 0
#%%
#populating dict['Values']
for df in happyDFs:
    for index, row in df.iterrows():
        if row['Country'] in (countries):
            Happy[row['Country']]['Values'].append(round(row['Happiness Score'],2))
            Freedom[row['Country']]['Values'].append(round(row['Freedom'],2))
            GDP[row['Country']]['Values'].append(round(row['Economy (GDP per Capita)'],2))

#populating dict['Correlation']
for country in countries:
    Happy[country]['Correlation'] = round(st.pearsonr(Elon, Happy[country]['Values'])[0],2)
    Freedom[country]['Correlation'] = round(st.pearsonr(Elon, Freedom[country]['Values'])[0],2)
    GDP[country]['Correlation'] = round(st.pearsonr(Elon, GDP[country]['Values'])[0],2)

print('***CHOMP***')
#%%
print('====Packaging Data====')

#Packaging the data into a format friendly to be stored in MongoDB

lists = {
    'Name':'Lists',
    'Elon':Elon,
    'Years':years,
    'Countries':countries,
    'Tweets':tweets
}

#Getting the country polygons
shapes = []
for feature in shapes_json['features']:
    if feature['properties']['ADMIN'] in countries:
        feature['Name'] = feature['properties']['ADMIN']
        feature['properties']['freedom'] = {}
        feature['properties']['freedom']['values'] = Freedom[feature['properties']['ADMIN']]['Values']
        feature['properties']['freedom']['correlation'] = Freedom[feature['properties']['ADMIN']]['Correlation']
        feature['properties']['happiness'] = {}
        feature['properties']['happiness']['values'] = Happy[feature['properties']['ADMIN']]['Values']
        feature['properties']['happiness']['correlation'] = Happy[feature['properties']['ADMIN']]['Correlation']
        feature['properties']['correlation'] = Happy[feature['properties']['ADMIN']]['Correlation']
        feature['properties']['GDP'] = {}
        feature['properties']['GDP']['values'] = GDP[feature['properties']['ADMIN']]['Values']
        feature['properties']['GDP']['correlation'] = GDP[feature['properties']['ADMIN']]['Correlation']
        shapes.append(feature)

#Replacing them with these smaller polygons to load quicker
for feature in small_shapes_json['features']:
    for shape in shapes:
        if feature['properties']['A3'] == shape['properties']['ISO_A3']:
            shape['geometry'] = feature['geometry']

print('***CHOMP***')
print('====Spitting data====')
#Putting files into the MongoDB
# try:
#     client.drop_database('Elon_db')
# except:
#     pass
# elon_db.insert_one(lists)
# for shape in shapes:
#     elon_db.insert_one(shape)

#%%
#Attempt to retrofit existing code to spit out a json so the front end can be divorced from the back end
json_dict = {
    "type": "FeatureCollection",
    "features": []
}
for feature in shapes:
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
    json_dict["features"].append(new_entry)
# %%
