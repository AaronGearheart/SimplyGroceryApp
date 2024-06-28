import requests
import base64
import json
import os

def get_access_token(credentials, scope):

    token_url = 'https://api.kroger.com/v1/connect/oauth2/token'

    data = {
        'grant_type': 'client_credentials',
        'scope': scope
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {credentials}'
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:

        token_data = response.json()
        access_token = token_data['access_token']
        return access_token
    else:
        return None

def get_locations(zipcode):

    script_dir = os.path.dirname(__file__)  

    secrets_path = os.path.join(script_dir, 'secrets.json')

    with open(secrets_path, 'r') as f:
        secrets = json.load(f)

    client_id = secrets['kroger_client_id']
    client_secret = secrets['kroger_client_secret']
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    location_url = f"https://api.kroger.com/v1/locations?filter.zipCode.near={zipcode}&filter.radiusInMiles=10"
    location_access_token = get_access_token(credentials, '')
    if not location_access_token:
        return None

    location_headers = {
        "Authorization": f"Bearer {location_access_token}",
        "Cache-Control": "no-cache"
    }
    location_response = requests.get(location_url, headers=location_headers)
    if location_response.status_code == 200:

        location_data = location_response.json()

        locations = location_data["data"]

        location_dict = {}

        for location in locations:

            location_id = location["locationId"]
            address_line1 = location["address"]["addressLine1"]

            location_dict[location_id] = address_line1
        return location_dict
    else:
        return None