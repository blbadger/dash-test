import json
import pandas as pd

df = pd.read_csv('data/fips-unemp-16.csv', dtype={"fips": str})
df = pd.DataFrame(df)

def match_labels(df):
	# import json object for mapping data to US counties, labelled by fips
	with open('data/geojson-counties-fips.json') as response:
		counties = json.load(response)

	counties = counties['features']

	county_dict = {}
	for county in counties:
		props = county['properties']
		county_dict[int(props['GEO_ID'][-5:])] = props['NAME']


	df['cname'] = [0 for i in range(len(df['fips']))]

	for i in range(len(df['cname'])):
		if int(df['fips'][i]) in county_dict:
			df['cname'][i] = county_dict[int(df['fips'][i])]

	df.to_excel('extended_fips.xlsx')

match_labels(df)


