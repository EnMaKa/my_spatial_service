 # -*- coding: utf-8 -*-
from flask import Flask, g, request, jsonify
import sqlite3  
import sys

#for system encoding 
reload(sys)
sys.setdefaultencoding('utf-8')


## from helloworld example 
app = Flask(__name__, static_url_path='')

#for testing enter the dbpath
db_path = '/home/ma/my_bremen_osm_1.sqlite'

#make connection to the given db
def connect_db():
    return sqlite3.connect(db_path)


#show db-entry within the buffer of the given coords 
# @param lat,lon, buffer_size int
# @return db_entry str
def show_db(lat, lon, buffer_size):

    #given coordinates
    print "lat: %s" %(lat)
    print "lon: %s" %(lon)
    

    # Check for non-empty buffer_size
    if buffer_size == 0:
        buffer_size = 200

    print "buffer size: %s" %(buffer_size)

    cursr = g.db.cursor()
    #get the osm addresses from the test osm db
    #cursr.execute('''SELECT adress FROM my_osm_new_adresses ''')
    #print cursr.fetchall()
    cursr.execute(('''
        SELECT adress FROM my_osm_new_adresses as A
        WHERE Contains( 
            ST_Buffer(GeomFromText('POINT({0} {1})'), {2}),
            A.geom
            )
        AND A.ROWID IN (
          SELECT ROWID 
          FROM SpatialIndex
          WHERE f_table_name = 'my_osm_new_adresses' 
          AND search_frame = ST_Buffer(GeomFromText('POINT({0} {1})'), {2})
        )
        ''').format(lat, lon, buffer_size)) 
    db_entries = cursr.fetchall()

    #convert to string
    return str(db_entries[0][0] + ", " +db_entries[1][0])
   

# show entries on db with address name 
# @return adress string 
def get_address(address_name):
    print "Address called: %s" %(address_name)

    cursr = g.db.cursor()

    cursr.execute(('''
        SELECT adress, ST_X(geom), ST_Y(geom) FROM my_osm_new_adresses 
        WHERE adress LIKE '%{0}%'
        ''').format(address_name))

    db_addresses = cursr.fetchall()

    # TODO: transform GEOM into X and Y Coords
    print db_addresses [0][1]
    print db_addresses [0][2]
    print db_addresses [0][0]
    print db_addresses [1][0]


    ##str(str(db_addresses [0][0]) +" is located at Postiton: " + str(db_addresses [0][1]) + "," + str(db_addresses [0][2]))
    retrunVal = jsonify(
            adress=db_addresses [0][0],
            lat=db_addresses [0][1],
            lon=db_addresses [0][2]
        )
    #return db entry
    return retrunVal


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

# set root path and
# return static html page
@app.route('/')
def root():
    return app.send_static_file('index.html')


#get the geocoordinates from url and make a db call 
@app.route('/geocode')
def geocode():

    #get info from url 
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    buffer_size=request.args.get('buffer_size')

    #check for lat/lon if there are no coords, then return without db connection 
    if not lat and not lon:
        return 'No coords are given'

    # set default buffersize when no is given
    if not buffer_size:#
        buffer_size=200
        #return buffer_size

    #make db call 
    entry = show_db(lat,lon,buffer_size)

    print entry

    #give information about the coords
    ##return 'Recived coordinates: lat: %i lon: %i. Addres(ses) are:%s' % (int(lat),int(lon), entry);

    return entry

# API call to do a adress search based on adress name
@app.route('/locatestreet')
def locate_street():

    print "#### function locatestreet is called ####"

    address = request.args.get('address')

    address_entry = get_address(address)

    return address_entry 

# Errorhandling for invalid requests
@app.errorhandler(500)
def handle_bad_request(e):
    return 'Could not get any db entry, try later'

app.register_error_handler(500, lambda e: 'Could not get any entry to this location! - Sorry dude!')




'''

methods=['GET','POST']
    # check which type was called 
    if request.method == 'POST':
        print "##### POST METHOD IS CALLED #####"
        address_form = request.form['address']
        return address_form

    elif request.method == 'GET':
        print "##### GET METHOD IS CALLED #####"
        address_form = request.form['address']
        print address_form
        return "GET WAS CALLED"

    else:
        address_name = request.args.get('address')
        return address_name 
'''

   
    
