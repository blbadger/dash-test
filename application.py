#! python3 app.py
## Tests choropleth dashboarding with python dash using plotly
# Modified for faster response time (originally ~7s per input)

# import libraries
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import flask


dash_app = dash.Dash(title='Choropleth dash test')
# app has to be callable
app = dash_app.server

# import json object for mapping data to US counties, labelled by fips
with open('data/geojson-counties-fips.json') as response:
	counties = json.load(response)

# import unemployment data mapped to county via fips and convert to DataFrame object
df = pd.read_excel('data/extended_fips.xlsx', dtype={"fips": str})
df = pd.DataFrame(df)

states_list = ['DC', 'NC', 'PA', 'CA', 'AK', 'AZ', 'TX', 'All']

colors = {
	'background': '#D1D0D6',
	'text': '#10110'
}

# data processing switched to back-end for faster user response
coordinates = [[38.9072, -77.0369], 
				[35.5, -79.0193], 
				[41.2033, -77.1945], 
				[36.7783, -119.43], 
				[64.2008, -149.4937], 
				[34.0489, -111.0937], 
				[32.4487, -99.7331], 
				[53.5, -130]]

zooms = [8, 6, 6, 4.5, 3, 5, 4.5, 2]

state_codes = ['11', '37', '42', '06', '02', '04', '48'] 
states_list = ['DC', 'NC', 'PA', 'CA', 'AK', 'AZ', 'TX', 'All']

mapstyles = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner", "stamen-watercolor"]


# page layout and inputs specified
dash_app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': 'sans-serif'}, children=[
	html.Div(children=[
			html.H1(
				children='Dash Test in Development',
				style={
					'textAlign': 'left',
					'color': colors['text'],
					'margin-top': '0vh',
					'margin-left': '5vw',
					'width': '30vw'
				}

			),
			html.Div(children='Choropleth plot for employment in counties with range, state, and map choice', style={
				'textAlign': 'left',
				'color': colors['text'],
				'margin-bottom': '1vh', 
				'margin-top': '1vh',
				'margin-left': '3vw',
			})
		], 
		style={
		'backgroundColor': colors['background'],
		'font-family': 'sans-serif',
		'display': 'inline-block',
		'margin-left': '17vw'
		}
	),

	html.Div(
		children=[
		html.Label('Select map style: ',
			style={'font-weight': 'bold',
			'display':'inline-block'}),
		dcc.Dropdown(
				id='mapstyle',
				options=[{'value': x, 'label': x} 
						 for x in mapstyles],
				value='carto-positron',
				style={
					'width': '12vw'}
		)],
		style={'display': 'inline-block',
				'margin-left': '5vw',
				'vertical-align': 'top',
				'padding-top': '1vh'
				}
		),

	dcc.Graph(id='choropleth', 
		style={
			'height': '90vh'
		}),

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

    html.Div(id='output-container-range-slider', 
    	style={
    		'textAlign': 'center',
    		'font-family': 'sans-serif', 
    		'font-weight': 'bold'
    	}),

    html.Br(),

	html.Label('Select State: ', 
		style={
			'font-weight': 'bold',
			'margin-left': '2vw'
		}),

	dcc.RadioItems(
		id='states', 
		options=[{'value': x, 'label': x} 
				 for x in states_list],
		labelStyle={'margin-left': '0.5vw'},
		value=states_list[-1],
		style={'display': 'inline-block',
				'width': '35vw',
				'margin-bottom': '5vh'}
	)

])

# responsive callbacks
@dash_app.callback(Output(component_id='choropleth', component_property='figure'), 
			[Input(component_id='states', component_property='value'),
			 Input(component_id='range-slider', component_property='value'),
			 Input(component_id='mapstyle', component_property='value')])
def display_choropleth(states_value, slider_value, mapstyle_value):
	i = states_list.index(states_value)
	pair = coordinates[i]
	zoom = zooms[i]
	if i < len(states_list) - 1:
		state_code = state_codes[i]
	else:
		state_code = ''

	 # matches to all entries in df with fips[0:2]
	state_df = df[df['fips'].str.match(state_code)]

	fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=state_df.fips, z=state_df.unemp,
						   colorscale="Viridis",
						   marker_opacity=0.5,
						   marker_line_width=0,
						   zmin=0,
						   zmax=12,
						   colorbar_title= "% Unemp.",
						   text=state_df['cname']
						  ))

	fig.update_layout(mapbox_zoom=zoom, 
					  mapbox_center = {"lat": pair[0], "lon": pair[1]},
					  mapbox_style=mapstyle_value,
					  margin={"r":0,"t":0,"l":0,"b":0},
					  plot_bgcolor='rgba(0,0,0,0)'
				)

	fig.update_traces(
		zmin=slider_value[0],
		zmax=slider_value[1]
		)

	return fig

# percentage range slider label output
@dash_app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('range-slider', 'value')])
def update_output(value):
    return 'Range selected: {} to {} %'.format(value[0], value[1])

# for running on azure
if __name__ == '__main__':
	# for testing
	# dash_app.run_server(debug=True, port=8022)
    dash_app.run_server(debug=True)
