#%%
import pandas as pd
import json
import os
from pprint import pprint

#%%
filepath = os.path.join("..","Data","countries.geojson")
with open(filepath) as jsonfile:
    shapes_json = json.load(jsonfile)

elon = pd.read_csv("../Data/elonmusk.csv")
# %%
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
print(Elon)


# %%


###'years' carries the list of years###
years = [2015,2016,2017,2018,2019,2020]

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

shapes = {}
for feature in shapes_json['features']:
    if feature['properties']['ADMIN'] in countries:
        shapes[feature['properties']['ADMIN']] = feature['geometry']['coordinates']

#6 countries are not represented in 'shapes' so we need to remove these from countries
#Names maually changes so there are no more mismatches
for country in countries:
        if country not in shapes.keys():
            print(country)
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
for df in happyDFs:
    for index, row in df.iterrows():
        if row['Country'] in (countries):
            try:
                Happy[row['Country']]['Values'].append(row['Happiness Score'])
                Freedom[row['Country']]['Values'].append(row['Freedom'])
                GDP[row['Country']]['Values'].append(row['Economy (GDP per Capita)'])
            except:
                pass


#%%


pprint(len(countries))
# %%
