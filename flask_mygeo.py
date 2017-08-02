from flask import Flask, g, request
import sqlite3  

## from helloworld example 
app = Flask(__name__)
#for testing enter the dbpath
dbPath = '/home/ma/my_bremen_osm_1.sqlite'


#make connection to the given db
def connect_db():
    return sqlite3.connect(dbPath)


#show db-entry within the buffer of the given coords 
# @param lat,lon int
def show_db(lat, lon):
        
    #buffer coordinates
    buffLat = lat
    buffLon = lon

    print "lat: %s" %(lat)
    print "lon: %s" %(lon)
    print "buffer lat: %s" %(buffLat)
    print "buffer lon: %s" %(buffLon)

    cursr = g.db.cursor()
    #get the osm addresses from the test osm db
    #cursr.execute('''SELECT adress FROM my_osm_new_adresses ''')
    #print cursr.fetchall()
    cursr.execute(('''
        SELECT * FROM my_osm_new_adresses as A
        WHERE Contains( 
            ST_Buffer(GeomFromText('POINT(%s %s)'), 200),
            A.geom
            )
        AND A.ROWID IN (
          SELECT ROWID 
          FROM SpatialIndex
          WHERE f_table_name = 'my_osm_new_adresses' 
          AND search_frame = ST_Buffer(GeomFromText('POINT(%s %s)'), 200)
        )
        ''') %(lat,lon,buffLat,buffLon))
    print cursr.fetchall()

      

#before every request a connection to the db is set 
@app.before_request
def before_request():    
    g.db = connect_db()
    #load spatialite extension
    g.db.execute("select load_extension('/usr/local/lib/mod_spatialite')")


#after the request the connection should be closed
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def hello_world():
    return 'Hello, World! Nice to meet you!'


#get the geocoordinates from url and make a db call 
@app.route('/geocode')
def geocode():   
    #get lat/lon from url 
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    #check for lat/lon if there are no coords, then return without db connection 
    if not lat and not lon:
        return 'No coords are given'

    #make db call 
    show_db(lat,lon)

    #give information about the coords
    return 'Recived coordinates: lat: %i lon: %i' % (int(lat),int(lon));
    
    
