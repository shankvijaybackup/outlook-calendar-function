from dotenv import load_dotenv
import os
import requests


# Load environment variables from .env file
load_dotenv()

def get_access_token():
    tenant_id = os.getenv("MS_TENANT_ID")
    client_id = os.getenv("MS_CLIENT_ID")
    client_secret = os.getenv("MS_CLIENT_SECRET")
    scope = "https://graph.microsoft.com/.default"

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, data=payload)
    
    if response.status_code != 200:
        print(f"Token request failed: {response.text}")
        raise Exception(f"Token request failed: {response.text}")
    
    return response.json()["access_token"]
