import requests
from flask import current_app

def setup_ais_token():
    url = "https://id.barentswatch.no/connect/token"
    payload = {
        "client_id": "havard.langdal.hovde@innovasjonnorge.no:acdc",
        "client_secret" : "test123456789",
        "grant_type": "client_credentials"
    }
    req = requests.post(url, data= payload)
    access_token = req.json()["access_token"]
    return access_token

def get_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept" : "application/json"
    }

def get_request_json(coords):
    return {
        "msgtimefrom": "2023-02-09T00:00:00+00:00",
        "msgtimeto": "2023-02-09T23:59:00+00:00",
        "polygon": {
            "coordinates": [coords],
            "type": "Polygon"
        }
    }

def make_request(coords, headers):
    url = "https://historic.ais.barentswatch.no/v1/historic/mmsiinarea"
    json = get_request_json(coords)
    res = requests.post(url, headers = headers, json = json)
    return res

def get_ais_data(coords):
    access_token = current_app.config["ais_token"]
    headers = get_headers(access_token)
    res = make_request(coords, headers)
    if res.status_code != 200:
        access_token = setup_ais_token()
        current_app.config["ais_token"] = access_token
        headers = get_headers(access_token)
        res = make_request(coords, headers)
    return res.json()
