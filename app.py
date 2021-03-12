#! python3 dash_test.py
## Tests choropleth dashboarding with python dash using plotly
# Very good detail but slower response time (~5s per state input)

# import libraries
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from urllib.request import urlopen
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.express as px

# import json object for mapping data to US counties, labelled by fips
with open('data/geojson-counties-fips.json') as response:
	counties = json.load(response)

# import unemployment data mapped to county via fips and convert to DataFrame object
df = pd.read_csv('data/fips-unemp-16.csv', dtype={"fips": str})
df = pd.DataFrame(df)

app = dash.Dash()

states_list = ['DC', 'NC', 'PA', 'CA', 'AK', 'All']

colors = {
	'background': '#D1D0D6',
	'text': '#10110'
}

markdown_text = '''

### Test for markdown features

*Markdown* is useful to write 

```
# code
def function(args, **kwargs):
	return 0 ** 1
``` 

as well as other text

'''

# page layout and inputs specified
app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'sans-serif'}, children=[
	html.H1(
		children='Dash Test in Development',
		style={
			'textAlign': 'center',
			'color': colors['text']
		}

	),
	html.Div(children='Choropleth plot for employment in counties with state and range choice', style={
		'textAlign': 'center',
		'color': colors['text']
	}),

	dcc.Graph(id='choropleth'),

	dcc.RangeSlider(
        id='range-slider',
        min=0,
        max=20,
        step=0.5,
        value=[0, 20],
        marks={
        	0: {'label': '0 %'},
        	5: {'label': '5 %'},
        	10: {'label': '10 %'},
        	15: {'label': '15 %'},
        	20: {'label': '20 %'}
        }
    ),

    html.Div(id='output-container-range-slider'),

    html.Br(),

	html.Label('Select State: '),

	dcc.RadioItems(
		id='states', 
		options=[{'value': x, 'label': x} 
				 for x in states_list],
		value=states_list[-1],
		labelStyle={'display': 'inline-block'}
	),

	html.Div([
	dcc.Markdown(children=markdown_text)
	])
])

# responsive
# @app.callback(Output(component_id='choropleth', component_property='figure'), 
# 			[Input(component_id='states', component_property='value'),
# 			 Input(component_id='range-slider', component_property='value')])
# def display_choropleth(states_value, slider_value, states_list = ['DC', 'NC', 'PA', 'CA', 'AK', 'All']):
# 	# list of coordinates and viewing scales for each possible state
# 	coordinates = [[38.9072, -77.0369], [35.5, -79.0193], [41.2033, -77.1945], [36.7783, -119.43], [64.2008, -149.4937], [53.5, -130]]
# 	zooms = [8, 6, 6, 4.5, 3, 2]

# 	# DC, NC, CA, and AK, respectively
# 	state_codes = ['11', '37', '42', '06', '02'] 

# 	for i in range(len(states_list)):
# 		if states_list[i] == states_value:
# 			pair = coordinates[i]
# 			zoom = zooms[i]
# 			if i < 5:
# 				state_code = state_codes[i]
# 			else:
# 				state_code = ''

# 	state_df = df[df['fips'].str.match(state_code)] # matches to all entries in df with fips[0:2] == predicate

# 	## if the initial range is desired to be set to min-max employment rates

# 	# unemp_rates = state_df['unemp']
# 	# ls = []
# 	# for item in range(len(unemp_rates)):
# 	# 	ls.append(unemp_rates[item])

# 	# ls.sort()
# 	# smallest = ls[0]
# 	# largest = ls[-1]

# 	# Make the figure with responsive range_color and zoom args
# 	fig = px.choropleth_mapbox(state_df, geojson=counties, locations='fips', color='unemp',
# 						   color_continuous_scale="Viridis",
# 						   range_color=(slider_value[0], slider_value[1]),
# 						   mapbox_style="carto-positron",
# 						   zoom=zoom, center = {"lat": pair[0], "lon": pair[1]},
# 						   opacity=0.3,
# 						   labels={'unemp':'unemployment rate'}
# 						  )

# 	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# 	return fig

# # percentage range slider label output
# @app.callback(
#     dash.dependencies.Output('output-container-range-slider', 'children'),
#     [dash.dependencies.Input('range-slider', 'value')])
# def update_output(value):
#     return 'Range selected: {} to {} %'.format(value[0], value[1])

# run the app on a local host
if __name__ == '__main__':
	app.run_server(debug=True)

