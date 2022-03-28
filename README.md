hosting
button used

# Kratsas Records
An interview project built using Dash written in Python, Kratsas Records, takes the data inside accidents.parquet and displays it so the user may interact and understand it.

## Setup

To run the program:
1. Make sure you are at the root of the project.
2. pip install -r requirements.txt
3. *python or python3* coffee_records_app.py

If any changes are made to the React code "npm run build" must be ran

## Code
The project consists of four main files
1. coffee_records_app.py: The starting file where the Dash application is started and maintained.
2. coffee_records_functions.py: Several functions that are used inside CRA, some are used more than once, others are in the seperate file for readibility. 
3. coffee_records_test.py: Test for main parquet searching function.
4. SearchBar.react.js: A React component that the user may interact with to query the DataTable.

## UX
The Dash Layout consists of the following components:
    -Title, Subtitle
    -Searchbar: user can enter and search a string of text to see where it appears in the database. This can sometimes take a while to update.
    -Mapbox Map: Starts with a zoomed out map of all accidents, when a user clicks on a row, it zooms in to the specific incident, can be hovered over to show data.
    -Datatable: Table showing all the data from the stored accidents.parquet to start, and will change based on the users searched term.
    -Vehicle Plot: A scatterplot of Model vs Make, with the color being Year, and size being number.

## Further improvements
    - Increased styling changes, mainly to the title, and the background of the page.
    - Added React components, the first of which would be a menu bar, breaking out the application into different webpages: map, plot, table etc.
    - Showing the terms that the different weather,road conditions represent.
    - The tool used for the latitude/longitude, did not work as well as intended, some locations were not found, leaving to some inaccurate map markers.
    - Host the application on GCP/AWS.
    
## Sources
    https://medium.com/@whwrd/building-a-beautiful-text-input-component-in-react-f85564cc7e86
    https://www.mapbox.com/
    https://dash.plotly.com/
