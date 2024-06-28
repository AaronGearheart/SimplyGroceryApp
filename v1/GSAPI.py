import requests
import json
import os

def update_list(uid, lid, fulfillment):
    url = 'https://gearheartstudios.pythonanywhere.com/updatelist'
    
    script_dir = os.path.dirname(__file__)  

    secrets_path = os.path.join(script_dir, 'secrets.json')

    with open(secrets_path, 'r') as f:
        secrets = json.load(f)
        
    api_key = secrets['gsapi_key']
    
    # Define the request headers
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json',
        'LocationID': lid,
        'UserID': uid,
        'Fulfillment': fulfillment
    }
    
    response = requests.post(url, headers=headers)
    
    return response.text
