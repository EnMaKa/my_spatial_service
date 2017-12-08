###### This is a read me file for my project for documentation issues

## My geocoder example

This is a study project to create a reverse geocoding application based on flask and a sqlite data base. The flask application provides a small webpage with a leaflet.js application running on it. The database is build on OpenStreetMap (OSM) data. The OSM-data was downloaded from [Geofabrik](http://www.geofabrik.de) and was edited with the sqlite extension spatialite (version 4). 

To be able to use a reverse geocoder, it was necessary to select the node information (the node ids and their geometry) and the adresses which are connected to the node id. 


##### Frameworks used

For this project I used: 

- Flask (version 0.12.2)
- Leaflet 
- SQLite (version 3.9.2)
- SQLite extension Spatialite (version 4.3.0a)
- SQLIte extension Spatialite-tools (version 4.3.0)
- ReasOSM (version 1.0.0)


### Get the project started

Description how to set up the project on own system.

#### Install Frameworks

For this project I used the frameworks listed above and with some scripts they'll install very easy just look [here](https://github.com/EnMaKa/my_spatial_service/tree/master/libs). 

You just to have install them by cmd e.g `sudo ./NameOfScript`
or step by step:
##### Example: ReadOSM
`wget http://www.gaia-gis.it/gaia-sins/readosm-1.0.0e.tar.gz

tar -xvzf readosm-1.0.0e.tar.gz 

cd readosm-1.0.0e/

./configure

make -j8

sudo make install-strip`


The tools have some install scripts which you can use or you just download and install the packages via pip or something else. If the scripts should not work, the you can simple copy the cmd info and paste it into your cmd.

#### Data
Like I said, the used data for this geocoder example is ready to download at [Geofabrik](http://www.geofabrik.de). There I used the OSM database file for Bremen (bremen-latest.osm.pdf).

To set up the SQLite database with the osm-raw information you just have to make this call in cmd
`spatialite_osm_raw -o my_country.osm.pbf -d my_country.sqlite`


For a reverse geocoder it is necessary to connect the node information with the adresses that belongs to the node.id with their geometry. Therefore I used some SQL-Statements that you will find in the uploaded SQLscript [here](https://github.com/EnMaKa/my_spatial_service/blob/master/sql_statements.sql). Just ran each step alone to set up the database.

1. Create table with node.id, address and  then add geometry column
2. Create another table with the merged node informations from other tabels
3. Transfer information info first table
4. Create spatial index for faster search results

#### Flask
For this project I used Flask as backend service. For those never worked with Flask - it is written in python and in my opion pretty easy as node.js to start with. 

The flask backend will provide information about coordinates and streetnames. 

Extesions used:
- g 
- request 
- jsonify
- sqlite3 
- sys

#### Make an API-Call
When the server runs, you can make two different calls to get informations from the database.

##### 1. Get coordination based information
The first call makes an request to the spatialite DB to get the address name and number based on coordinations.

1. Example: http://127.0.0.1:5000/geocode?lat=981325&lon=6997858 

2. Exmaple: http://127.0.0.1:5000/geocode?lat=981325&lon=6997858&buffer_size=150

##### 2. Get Adresses based information
The second call will look at the informations that are given with a certain streetname.

Example: http://127.0.0.1:5000/locatestreet?address=Brüggeweg

The Flask-Backend will provide a simple JSON file with the first matching entry from the SQLite DB.


#### Known Issues
The OSM node informations could not be called like they should. You get an address near to the lokation you've clicked, but not the right. There fore you could adjust the buffer radius at the mouseclick function in the map.js.

Another bug is the jump to address function if you search for an address. I used Proj4 to get the right coordinates but somehow this works not like expecting.

The Coordinates from clickevent seem to be right, if you transform coords from DB the lat-Value seems about faktor 10 to high, even lon-Value is not that right. It could be a transformation issue in the database for the entries from OSM.


