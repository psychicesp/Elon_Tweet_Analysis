#%%
import pandas as pd
from pprint import pprint
#%%

elon = pd.read_csv("../CSVs/elonmusk.csv")
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

elon_tweets = elon_year['conversation_id'].tolist()
print(elon_tweets)

output_dict['elon'] = elon_tweets
# %%
file_structure = '../CSVs/Happiness/'
years = [2015,2016,2017,2018,2019,2020]

happyDFs = []

for i in years:
    happyDFs.append(pd.read_csv(f"{file_structure}{str(i)}.csv"))

countries = happyDFs[0]['Country'].tolist()


for country in countries:
        output_dict[country] = {}
        output_dict[country]['Geometry'] = []
        output_dict[country]['Happiness']= {}
        output_dict[country]['Happiness']['Values'] = []
        output_dict[country]['Happiness']['Correlation'] = 0
        output_dict[country]['Freedom']={}
        output_dict[country]['Freedom']['Values']= []
        output_dict[country]['Freedom']['Correlation'] = 0
        output_dict[country]['GDP']={}
        output_dict[country]['GDP']['Values'] = []
        output_dict[country]['GDP']['Correlation'] = 0
print(len(countries))
#%%
for df in happyDFs:
    for country in countries:
        df_countries = df['Country'].tolist()
        if country not in df_countries:
            countries.remove(country)
print(len(countries))
#%%
for df in happyDFs:
    for index, row in df.iterrows():
        if row['Country'] in (countries):
            try:
                output_dict[row['Country']]['Happiness']['Values'].append(row['Happiness Score'])
                output_dict[row['Country']]['Freedom']['Values'].append(row['Freedom'])
                output_dict[row['Country']]['GDP']['Values'].append(row['Economy (GDP per Capita)'])
            except:
                pass
pprint(output_dict)