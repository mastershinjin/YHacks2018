CLIENT_ID = '6e0a0f53-5e65-4dbf-bab0-087f0d1d48fe'
CLIENT_SECRET = '57479324-a7d4-4257-b040-52840d31d553' #secret key generated... don't lose
import smartcar
from flask import Flask, request, jsonify
import sys, os
import time

file_dir = os.path.dirname("/Users/robertyang/PycharmProjects/backend/SmartCar_Backend/SQlitetest.py")
sys.path.append(file_dir)

import SQlitetest

access = None;

# 1. Create an instance of Smartcar's client.
client = smartcar.AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri='http://localhost:8000/callback', #how do we add multiple redirect URIs?
    scope=['read_vehicle_info', 'read_location', 'control_security'],
    test_mode = True
)

# 2. Create a new webserver with the Flask framework.
app = Flask(__name__)

# 3. Create a page with a 'Connect Car' button.
@app.route('/', methods=['GET'])
def index():
    auth_url = client.get_auth_url(force=True)
    return '''
        <h1>Hello, World!</h1>
        <a href=%s>
          <button>Connect Car</button>
        </a>
    ''' % auth_url # generate the url using the js sdk

# 4. On an HTTP GET to our callback will exchange our OAuth Auth Code
#    for an Access Token and log it out.


@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    global access
    access = client.exchange_code(code)

    # Log the access token response
    print(access)

    # Respond with a success status to browser
    return jsonify(access)


#get the vehicle location in lat + long [json], also check boundaries

@app.route('/location', methods=['GET'])
def location():

    global access

    print(smartcar.get_vehicle_ids(access['access_token']));
    vehicleID = smartcar.get_vehicle_ids(access['access_token'])['vehicles'][0];
    vehicle = smartcar.Vehicle(vehicleID, access['access_token']);

    print(vehicle.location());
    new_access = client.exchange_refresh_token(access['refresh_token'])
    print(new_access);
    return jsonify(vehicle.location());


@app.route('/cars', methods=['GET'])
def cars():
    global access

    userVehicles = smartcar.get_vehicle_ids(access['access_token'])['vehicles'];

    list = []
    for vehicleID in userVehicles:
        vehicle = smartcar.Vehicle(vehicleID, access['access_token']);
        list.append(vehicle.info())

    return list

@app.route('/unlockAccess', methods=['GET'])
def unlockAccess(userAllowed, carID):
    if(userAllowed == True):
        vehicle = smartcar.Vehicle(carID, access['access_token']);
        # for demonstration purposes wait 5 sec (ideally person would arrive near car location and unlock:
        time.sleep(5)
        vehicle.unlock() #unlocks vehicle
    return userAllowed;

@app.route('/lockAccess', methods=['GET'])
def lockAccess(userAllowed, carID):
    if (userAllowed == True):
        vehicle = smartcar.Vehicle(carID, access['access_token']);
        #for demonstration purposes wait 5 sec (ideally person would arrive near car location and unlock:
        time.sleep(5)

        vehicle.lock() #locks vehicle
    return userAllowed;

#get's car info for a user based on the facebookID
@app.route('/getUserCar', methods=['GET'])
def getUserCar(facebookID):
    if(not SQlitetest.check_new_user(facebookID)):
        return SQlitetest.get_user_car_info(facebookID) #returns the JSON object
    else:
        return False;



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

@app.route('getUserInfo', methods=['GET'])
def getUserInfo(facebookID):
    return SQlitetest.user_info(facebookID) #JSON including user firstname, lastname, etc...





"""
def get_fresh_access():
    access = load_access_from_database()
    if smartcar.expired(access['expiration']):
        new_access = client.exchange_refresh_token(access['refresh_token'])
        put_access_into_database(new_access)
        return new_access
    else:
        return access



fresh_access_token = get_fresh_access()['access_token']
"""



# 5. Let's start up the server at port 8000.
if __name__ == '__main__':
    app.run(port=8000)



