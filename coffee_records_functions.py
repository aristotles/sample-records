import datetime
from flask import request
import pandas as pd
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go

#Scatterplot of Model vs Make, with color=Year, and size = number
def getVehicleMapPlot():

    #Loads originally given parquet, new one doesnt have same fields.
    originalDf = pd.read_parquet('original.parquet', engine='pyarrow')
    vehicleDataPlot = px.scatter(originalDf, x="MODEL", y="MAKE", color="MODEL_YEAR", size='INCIDENTS')
    vehicleDataPlot.update_layout(paper_bgcolor="rgb(0,0,0,0)",  font_color="white", title_font_family="Sans Serif",)
    return vehicleDataPlot
    
#Mapbox map of all locations for landing screen.
def getMainMap():

    df = pd.read_parquet('accidents.parquet', engine='pyarrow')
    df = df.apply(pd.to_numeric, errors='ignore')

    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="City",
                        color_discrete_sequence=["yellow"], zoom=3, height=300)

    #Normally I would use a secrets manager to encrypt an api token.
    fig.update_layout(mapbox_style='outdoors', margin={"r": 0, "t": 0, "l": 0, "b": 0},  mapbox=dict(
    accesstoken="pk.eyJ1IjoiZ2NwZDMzMCIsImEiOiJjamhjeHcyZW0waW42MzBzNjNmNnV4bmkzIn0.16YDsZzavkrzT-Y4DmWjiw",  center=go.layout.mapbox.Center(lat=39.8283,lon=-98.5795)))
    return fig;

#Creates a datatable using the passed term.
def getTable(passedTerm):
    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": ["", "Report Number"], "id": "Report Number"},
            {"name": ["", "Date"], "id": "Date"},
            {"name": ["", "Time"], "id": "Time"},
            {"name": ["Location", "City"], "id": "City"},
            {"name": ["Location", "State"], "id": "State"},
            {"name": ["Conditions", "Road Condition"], "id": "Road Condition"},
            {"name": ["Conditions", "Weather Condition"], "id": "Weather Condition"},
            {"name": ["Conditions", "Incidents"], "id": "Incidents"},
            {"name": ["Vehicle", "Vehicle"], "id": "Vehicle"},
            {"name": ["Vehicle", "VIN"], "id": "Vin"},

        ],
        merge_duplicate_headers=True,
        #Gets the dataframe for the passed term.
        data=searchRecords(passedTerm).to_dict('records'),
        style_cell=dict(textAlign='left',  fontFamily='sans-serif', paddingLeft='8px',paddingRight='8px' ),
        style_header=dict(backgroundColor="black", color='white', paddingLeft='8px', paddingRight='8px'),
        sort_action='native',
        page_size=20,
        sort_by=[{'column_id': 'REPORT_DATE', 'direction': 'desc'}],
    )


#Creates a dataframe with every row that matches the term is found in the searched column, then combines then.
def searchRecords(searchTerm):
    mainDataframe=pd.read_parquet('accidents.parquet', engine='pyarrow')
    mainDataframe1 = mainDataframe.loc[mainDataframe['City'].str.contains(searchTerm, case=False, regex=False)]
    mainDataframe2 = mainDataframe.loc[mainDataframe['State'].str.contains(searchTerm, case=False, regex=False)]
    mainDataframe3 = mainDataframe.loc[mainDataframe['Date'].astype(str).str.contains(searchTerm, case=False, regex=False)]
    mainDataframe4 = mainDataframe.loc[mainDataframe['Report Number'].str.contains(searchTerm, case=False, regex=False)]
    mainDataframe5 = mainDataframe.loc[mainDataframe['Road Condition'].astype(str).str.contains(searchTerm, case=False, regex=False)]
    mainDataframe6 = mainDataframe.loc[mainDataframe['Weather Condition'].astype(str).str.contains(searchTerm, case=False, regex=False)]
    mainDataframe7 = mainDataframe.loc[mainDataframe['Incidents'].astype(str).str.contains(searchTerm, case=False, regex=False)]
    mainDataframe8 = mainDataframe.loc[mainDataframe['Vin'].astype(str).str.contains(searchTerm, case=False, regex=False)]
    mainDataframe9 = mainDataframe.loc[mainDataframe['Vehicle'].str.contains(searchTerm, case=False, regex=False)]
    mainDataframe10 = mainDataframe.loc[mainDataframe['Time'].astype(str).str.contains(searchTerm, case=False, regex=False)]

    mainDataframe=pd.concat([mainDataframe1,mainDataframe2,mainDataframe3,mainDataframe4,mainDataframe5,mainDataframe6,mainDataframe7,mainDataframe8,mainDataframe9,mainDataframe10])
    
    return mainDataframe

#Some of the parquet changes I made throughout the course of development that only needed to be ran once.
def parquetManipulation():
    mainDataframe=pd.read_parquet('accidents.parquet', engine='pyarrow')

    #Formated the time to be more presentable.
    for index, row in mainDataframe.iterrows():
        if(len(str(row['REPORT_TIME']))>3):
            one=datetime.time(hour=int(str(row['REPORT_TIME'])[:-2]), minute=int(str(row['REPORT_TIME'])[2:4]))
        elif(len(str(row['REPORT_TIME']))>2):
            one=datetime.time(hour=int(str(row['REPORT_TIME'])[0:1]), minute=int(str(row['REPORT_TIME'])[1:3]))
        elif(len(str(row['REPORT_TIME']))>1):
            one=datetime.time(hour=0, minute=int(str(row['REPORT_TIME'])))
        else:
            one=datetime.time(hour=0, minute=0)
        mainDataframe.loc[index,'Time'] = one.strftime("%H:%M")

    #Some of the parquet changes I made.
    mainDataframe['CITY']=mainDataframe['CITY'].str.title()
    mainDataframe['MAKE']=mainDataframe['MAKE'].str.title()
    mainDataframe['MODEL']=mainDataframe['MODEL'].str.title()
    mainDataframe['MAKE']=mainDataframe['MAKE'].str.title()
    mainDataframe = mainDataframe.drop('MAKE', 1)
    mainDataframe = mainDataframe.drop('MODEL', 1)
    mainDataframe = mainDataframe.drop('MODEL_YEAR', 1)
    mainDataframe = mainDataframe.drop('REPORT_TIME', 1)
    mainDataframe= mainDataframe.rename(columns={'REPORT_NUMBER': 'Report Number', 'REPORT_DATE': 'Date', 'CITY': 'City','STATE': 'State', 'INCIDENTS':'Incidents', 'VIN': 'Vin',  'WEATHER_CONDITION': 'Weather Condition', 'ROAD_CONDITION': 'Road Condition'})
    
    #This was the code that was ran to get the latitude/longitude for each location. It took roughly an hour to run.
    for index, row in mainDataframe.iterrows():
        url = "https://nominatim.openstreetmap.org/?addressdetails=1&q=" + row['CITY'] + "+" + row['STATE'] +"&format=json&limit=1"

        response = request.get(url).json()
    
        if response:
            print((response[0]["lat"]))
            mainDataframe.loc[index,'latitude'] = (response[0]["lat"])
            mainDataframe.loc[index,'longitude'] = (response[0]["lon"])
        else:
            print('EMPTY........')
            mainDataframe.loc[index,'latitude'] = "0"
            mainDataframe.loc[index,'longitude'] = "0"
        count+=1

    #Exports/saves the parquet
    mainDataframe.to_parquet('mainDataframe.parquet.gzip', compression='gzip') 