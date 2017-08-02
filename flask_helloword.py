from flask import Flask, g, request
import sqlite3  


app = Flask(__name__)

dbName = 'PATH TO SQLite DB with OSM addresses'


def connect_db():
    return sqlite3.connect(dbName)

def show_db():
    print "fooo"
    cursr = g.db.cursor()
    cursr.execute('''SELECT adress FROM my_osm_new_adresses ''')
    print cursr.fetchall()
   # return 'connected to database'    

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def hello_world():
    return 'Hello, World! Nice to meet you!'

@app.route('/testing')
def testing():
    return 'Testingpage. Nothing more.'

@app.route('/geocode')
def geocode():   

    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat and not lon:
        return 'No coords are given'

    show_db()

    return 'Recived coordinates: lat: %s lon: %d' % (int(lat),int(lon));
    
    


'''
    dbName = 'my_bremen_osm_1.sqlite'
    # Do connection to database 
    dbConn = sqlite3.connect(dbName)

    # Cursor needed for SQL-statements
    cursr = dbConn.cursor()

    # Do SQL-statement 
    #cursr.execute("SELECT * FROM my_osm_new_adresses") 

    print cursr.fetchall()

    # Save (commit) the changes
   # dbConn.commit()

    # Close the connection
    dbConn.close()

'''

