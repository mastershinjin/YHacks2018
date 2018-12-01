CLIENT_ID = '6e0a0f53-5e65-4dbf-bab0-087f0d1d48fe'
CLIENT_SECRET = '57479324-a7d4-4257-b040-52840d31d553' #secret key generated... don't lose

import smartcar
from flask import Flask, request, jsonify


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


#get the vehicle location in lat + long [json]

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
        list.append(vehicle)

    return list



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



