###### This is a read me file for my project for documentation issues

### My geocoder example

This is a study project to create a reverse geocoding application based on flask and a sqlite data base. The flask application provides a small webpage with a leaflet.js application running on it. The database is build on OpenStreetMap (OSM) data. The OSM-data was downloaded from <http://www.geofabrik.de> and was edited with the sqlite extension spatialite (version 4). 

To be able to use a reverse geocoder, it was necessary to select the node information (the node ids and their geometry) and the adresses which are connected to the node id. 


##### Frameworks used

For this project I used: 

- Flak (version 0.12.2)
- Leaflet 
- SQLite (version 3.9.2)
- SQLite extension Spatialite (version 4.3.0a)
- SQLIte extension Spatialite-tools (version 4.3.0)

