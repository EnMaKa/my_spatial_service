from flask import Flask, g, request
import sqlite3  

## from helloworld example 
app = Flask(__name__)
#for testing enter the dbpath
dbPath = '/home/ma/my_bremen_osm_1.sqlite'


#make connection to the given db
def connect_db():
    return sqlite3.connect(dbPath)


#show db with every entry in cmd
def show_db():
    print "fooo"
    cursr = g.db.cursor()
    #get the osm addresses from the test osm db
    cursr.execute('''SELECT adress FROM my_osm_new_adresses ''')
    print cursr.fetchall()
      

#before every request a connection to the db is set 
@app.before_request
def before_request():    
    g.db = connect_db()
    #load spatialite extension
    g.db.execute("select load_extension('/usr/local/mod_spatialite.so')")


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
    show_db()

    return 'Recived coordinates: lat: %s lon: %d' % (int(lat),int(lon));
    
    
