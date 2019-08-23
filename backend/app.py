import smartcar
import sqlite3
import random
from flask import Flask, request, jsonify, redirect, g
from flask_cors import CORS

import sys, os
import time


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
CORS(app)

#absolute path to .db database, will change depending on user...(config?)
DATABASE = 'C:\Users\Robert Yang\Documents\YHacks2018-master\backend\users.db'

#code to retrieve database, only executed during active app context
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row #this will convert data retrieved from db from a tuple into a dictionary essentially
    return db

#function to do queries, "query" arg is a string in SQL to execute, and
#args is going to be whatever args you want to store results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

client = smartcar.AuthClient(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    redirect_uri=app.config["REDIRECT_URI"],
    test_mode=True
)

access = None
code = None
user_id = None
user_email = None
#code based off of smartcar api docs to automatically get a refresh Token
#obviously, you must have gone through the /exchange URI before you can run this method
def get_fresh_access():
    # this query should fetch ONLY ONE user from the database based on their user_id
    access = query_db('SELECT * FROM users_info WHERE userID = ?', [user_id], one=True)
    if smartcar.is_expired(access['expiration']):
        new_access = client.exchange_refresh_token(access['refresh_token'])
        #modify the database to reflect the change of tokens:
        query_db('UPDATE users_info SET access_tokens = ? WHERE userID = ?', [new_access, user_id], one=True)
        return new_access
    else:
        return access

#this will close connection with database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#we need something for the index/default page
@app.route('/')
def index():
    cur = get_db().cursor()
    #maybe some sort of HTML here?...

#going to add a separate login route
@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 1b: Launch Smartcar authentication dialog
    auth_url = client.get_auth_url()
    return redirect(auth_url)

# htpp://localhost:3000/exchange?code=<authorization_code>
@app.route('/exchange', methods=['GET'])
def exchange():
    # notice I made all these vars global just for simplicity sake, for a real secure application, this would not be the case...
    global code = request.args.get('code')
    #we need to account for when users deny permission for anything using exception handling:
    global access
    access = client.exchange_code(code)
    #getting their email:
    global user_email = request.form.get('email') #not sure if this will work since email/etc... is inputeed into smartcar connect?
    #generate a random userID:
    global user_id = random.randint(1,100) #if necessary, we can check to make sure the random int isn't in the database using SQL querying
    #here we insert values into the sql database:
    query_db('INSERT INTO users_info VALUES ?', [user_email, user_id, code, access], one=True)
    return '', 200

# htpp://localhost:8000/vehicles
@app.route('/vehicles', methods=['GET'])
def vehicles():
    global access
    access = get_fresh_access()
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    cars = []

    for id in vehicle_ids:
        vehicle = smartcar.Vehicle(id, access['access_token']);
        cars.append(vehicle.info())

    return jsonify(cars)

# htpp://localhost:8000/vehicle/<id>
@app.route('/vehicle/<vehicle_id>', methods=['GET'])
def vehicle(vehicle_id):
    global access
    access = get_fresh_access()
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
    info = vehicle.info()
    print(info)

    return jsonify(info)

# htpp://localhost:8000/vehicle/<id>/unlock
@app.route('/vehicle/<vehicle_id>/unlock', methods=['GET'])
def unlock(vehicle_id):
    global access
    access = get_fresh_access()
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
    response = vehicle.unlock()

    return jsonify(response) # 200 if succesful

# htpp://localhost:8000/vehicle/<id>/lock
@app.route('/vehicle/<vehicle_id>/lock', methods=['GET'])
def lock(vehicle_id):
    global access
    access = get_fresh_access()
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
    response = vehicle.lock()

    return jsonify(response) # 200 if succesful

# htpp://localhost:8000/vehicle/<id>/location
@app.route('/vehicle/<vehicle_id>/location', methods=['GET'])
def location(vehicle_id):
    global access
    access = get_fresh_access()
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token']);
    location = vehicle.location()
    # new_access = client.exchange_refresh_token(access['refresh_token'])

    return jsonify(location);
#logout endpoint to disconnet application for a particular vehicle
@app.route('/logout', methods=['GET'])
def logout(vehicle_id):
    global access
    close_connection() #this might be valid, might not be
    access = get_fresh_access()
    vehicle = smartcar.vehicle(vehicle_id, access['access_token']);
    vehicle.disconnet()


"""
#get's car info for a user based on the facebookID
@app.route('/getUserCar', methods=['GET'])
def getUserCar(facebookID):
    if(not SQlitetest.check_new_user(facebookID)):
        return SQlitetest.get_user_car_info(facebookID) #returns the JSON object
    else:
        return False;

###
#need to choose a car...
@app.route('/addUserToDatabase', methods=['GET'])
def addUserToDatabase(firstname, lastname, facebookID, carId):
    #for now defining carID to just be the first car:
    global access
    carId = smartcar.get_vehicle_ids(access['access_token'])['vehicles'][0];
    # first table:
    SQlitetest.car_data_entry(facebookID, smartcar.Vehicle(carId, access['access_token']))

    #second table:
    SQlitetest.data_entry_user_info(firstname, lastname, facebookID, access['access_token'],
                                    access['refresh_token_expiration'])
###
@app.route('/getUserInfo', methods=['GET'])
def getUserInfo(facebookID):
    return SQlitetest.user_info(facebookID) #JSON including user firstname, lastname, etc...

###
def get_fresh_access():
    access = load_access_from_database()
    if smartcar.expired(access['expiration']):
        new_access = client.exchange_refresh_token(access['refresh_token'])
        put_access_into_database(new_access)
        return new_access
    else:
        return access

###
fresh_access_token = get_fresh_access()['access_token']
"""

if __name__ == '__main__':
    app.run(port=3000)
