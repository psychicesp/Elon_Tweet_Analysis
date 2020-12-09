#%%
print('====Getting Imports====')
import pandas as pd
import json
import os
from scipy import stats as st
from pprint import pprint
import pymongo
print('***CHOMP***')
#%%
print("====Connecting to MongoDB====")
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Declare the database
db = client.Elon_db

# Declare the collection
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

elon.head()
# %%
output_dict = {}

elon_year = elon.groupby('year').agg({
    'conversation_id': 'count'
})
elon_year = elon_year.reset_index()

###'Elon' carries the list of elon tweet numbers!!###
Elon = elon_year['conversation_id'].tolist()

# %%
###'years' carries the list of years###
years = [2015,2016,2017,2018,2019,2020]
print('***CHOMP***')
print('====Parsing csvs====')
happyDFs = []
file_structure = '../Data/Happiness/'
for i in years:
    happyDFs.append(pd.read_csv(f"{file_structure}{str(i)}.csv"))
countries = happyDFs[0]['Country'].tolist()

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
lists = lists = {
    'Name':'Lists',
    'Elon':Elon,
    'Years':years,
    'Countries':countries
}

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

for feature in small_shapes_json['features']:
    for shape in shapes:
        if feature['properties']['A3'] == shape['properties']['ISO_A3']:
            shape['geometry'] = feature['geometry']
print('***CHOMP***')
print('====Spitting data====')
client.drop_database('Elon_db')
elon_db.insert_one(lists)
for shape in shapes:
    elon_db.insert_one(shape)

shapes_dict = {
    "type": "FeatureCollection",
    "features":shapes
}
#Writing the variables to JavaScript
file_name = os.path.join('..','JS','variables.js')
with open(file_name, 'w') as js_biggins:
    js_biggins.write(f"var shapes = {shapes_dict}\n")

with open(file_name, 'a') as js_biggins:
    js_biggins.write(f"var elon = {Elon}\n")
    js_biggins.write(f"var years = {years}\n")
    js_biggins.write(f"var countries = {countries}\n")
    js_biggins.write(f"var happy = {Happy}\n")
    js_biggins.write(f"var freedom = {Freedom}\n")
    js_biggins.write(f"var GDP = {GDP}\n")
    js_biggins.write(f"var hiddenMessage = 'you da best!'")
print('***spit***')
print("Finished Chewing")