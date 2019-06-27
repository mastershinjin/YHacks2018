import smartcar
from flask import Flask, request, jsonify
from flask_cors import CORS

import sys, os
import time

import SQlitetest

file_dir = os.path.dirname("/Users/robertyang/PycharmProjects/backend/SmartCar_Backend/SQlitetest.py")
sys.path.append(file_dir)

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
CORS(app)

client = smartcar.AuthClient(
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    redirect_uri=app.config["REDIRECT_URI"],
    test_mode=True,
)

access = None

# htpp://localhost:8000/exchange?code=<authorization_code>
@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')
    global access
    access = client.exchange_code(code)

    return '', 200

# htpp://localhost:8000/vehicles
@app.route('/vehicles', methods=['GET'])
def vehicles():
    global access
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
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
    info = vehicle.info()
    print(info)

    return jsonify(info)

# htpp://localhost:8000/vehicle/<id>/unlock
@app.route('/vehicle/<vehicle_id>/unlock', methods=['GET'])
def unlock(vehicle_id):
    global access
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
    response = vehicle.unlock()

    return jsonify(response) # 200 if succesful

# htpp://localhost:8000/vehicle/<id>/lock
@app.route('/vehicle/<vehicle_id>/lock', methods=['GET'])
def lock(vehicle_id):
    global access
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
    response = vehicle.lock()

    return jsonify(response) # 200 if succesful

# htpp://localhost:8000/vehicle/<id>/location
@app.route('/vehicle/<vehicle_id>/location', methods=['GET'])
def location(vehicle_id):
    global access
    vehicle = smartcar.Vehicle(vehicle_id, access['access_token']);
    location = vehicle.location()
    # new_access = client.exchange_refresh_token(access['refresh_token'])

    return jsonify(location);

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
    app.run(port=8000)
