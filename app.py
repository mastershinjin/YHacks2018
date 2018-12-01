CLIENT_ID = '6e0a0f53-5e65-4dbf-bab0-087f0d1d48fe'
CLIENT_SECRET = '57479324-a7d4-4257-b040-52840d31d553' #secret key generated... don't lose

import smartcar
from flask import Flask, request, jsonify

# 1. Create an instance of Smartcar's client.
client = smartcar.AuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri='http://localhost:8000/callback',
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
        <h1>Hello, World!</h1>jjj
        <a href=%s>
          <button>Connect Car</button>
        </a>
    ''' % auth_url

# 4. On an HTTP GET to our callback will exchange our OAuth Auth Code
#    for an Access Token and log it out.


@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    access = client.exchange_code(code)

    # Log the access token response
    print(access)

    # Respond with a success status to browser
    return jsonify(access)

# 5. Let's start up the server at port 8000.
if __name__ == '__main__':
    app.run(port=8000)