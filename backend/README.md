## Installation

Inside the root directory, use the following command to install the **required** dependencies.

```bash
$ pip install -r requirements.txt
```

## Usage

To make requests to Smartcar, we will need to provide our app secrets to the `smartcar.AuthClient`. We define the apps secret keys in an **[instance folder](http://exploreflask.com/en/latest/configuration.html#instance-folder)** so we don't expose them in version control.

Create the instance directory and config file:

```bash
$ mkdir instance && touch instance/config.py
```

Replace `config.py` with the following:

```python
# instance/config.py

CLIENT_ID="<client_id>"
CLIENT_SECRET="<client_secret>"
REDIRECT_URI="https://javascript-sdk.smartcar.com/redirect-2.0.0?app_origin=http://localhost:3000"
```

The `redirect_uri` is the same as the clients config. Read more on **[redirect_uri](https://smartcar.com/docs/integration-guides/react/setup/#3-configure-your-redirect-uri)**.

Now we can access the configuration keys via:
```python
# app.py

app.config["VAR_NAME"]
```
