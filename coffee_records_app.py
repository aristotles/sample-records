from dash import Dash, html, Input, Output, dcc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import search_bar
from coffee_records_test import runTests
from coffee_records_functions import getMainMap, getTable, getVehicleMapPlot, searchRecords

app = Dash("Coffee Insurance")

vehicleDataPlot=getVehicleMapPlot()
mainMap=getMainMap()

#Humor, its funny because its the other way to spell the word.
title = html.H1('Coffee Insurance Records')
subTitle = html.H4('The second best insurance a driver can get!')
searchBar = search_bar.SearchBar(
    id='input',
    value='',
    label='Search the records for:'
)

#Everything is styled from src/lib/fragments/style.css
app.layout = html.Div([
    title,
    subTitle,
    dcc.Graph(figure=mainMap, id='mapbox'),
    html.P(''),
    searchBar,
    html.P(''),
    html.H4(id='searchedForLabel', children=""),
    getTable(''),
    dcc.Graph(figure=vehicleDataPlot, id='vdp'),
])

#When the search button is pressed takes the text inside, searches for it, and updates the layout and label telling what was searched.
@app.callback(Output(component_id='searchedForLabel', component_property='children'), Input(component_id='input', component_property='value'), )
def display_output(input_value):
    if input_value:
        newText = "Searched for: " + input_value
        app.layout = html.Div([
            title,
            subTitle,
            dcc.Graph(figure=mainMap, id='mapbox'),
            html.P(''),
            searchBar,
            html.P(''),
            html.H4(id='searchedForLabel', children=newText),
            getTable(input_value),
            dcc.Graph(figure=vehicleDataPlot, id='vdp'),
        ])
        app.run_server(debug=False)


#When a cell is pressed, takes the location of the row and sets the map to zoom in/rerender for it.
@app.callback(
    Output('mapbox', 'figure'),
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell:
        #Loads the main new parquet.
        locationDf = searchRecords("")

        givenla = pd.to_numeric(locationDf.iloc[active_cell['row']]['latitude'], downcast="float")
        givenLat = [givenla]
        givenlo = pd.to_numeric(locationDf.iloc[active_cell['row']]['longitude'], downcast="float")
        givenLong = [givenlo]

        fig = go.Figure(go.Scattermapbox(
            lat=givenLat,
            lon=givenLong,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=80,
                opacity=0.3,
                color='darkorange'
            ),
            text=locationDf.iloc[active_cell['row']]['Report Number'],
        ))

        fig.update_layout(
            dragmode=False,
            hovermode='closest',
            mapbox=dict(
                accesstoken="pk.eyJ1IjoiZ2NwZDMzMCIsImEiOiJjamhjeHcyZW0waW42MzBzNjNmNnV4bmkzIn0.16YDsZzavkrzT-Y4DmWjiw",
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=givenla,
                    lon=givenlo
                ),
                pitch=0,
                zoom=9
            )
        )
        fig.update_layout(mapbox_style='satellite-streets')
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
    return mainMap
runTests()
app.run_server(debug=False)
