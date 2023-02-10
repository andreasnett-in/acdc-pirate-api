from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from flask import current_app
from PIL import Image
import io
import numpy as np

CLIENT_SECRET = "N&QBU3+>R}AJLqGQ(Z7?lTJ<.b8efeaR[p@xEWxw"
CLIENT_ID = "d03af2a2-acaa-40c8-b824-7eb237eca07e"

evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: { 
      bands: 3, 
      sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
    }
  }
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
}
"""

def setup_sentinel_token():
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
                          client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    access_token = token["access_token"]
    
    return oauth, access_token

def setup_sentinel_headers(token):
    url_request = 'https://services.sentinel-hub.com/api/v1/process'
    headers_request = {
    "Authorization" : f"Bearer {token}",
    "Content-Type" : "application/json"
    }

    return url_request, headers_request


def get_request_json(bbox):
    return {
    'input': {
        'bounds': {
            'bbox': bbox,
            'properties': {
                'crs': 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'
            }
        },
        'data': [
            {
                'type': 'S2L2A',
                'dataFilter': {
                    'timeRange': {
                        'from': '2023-01-01T15:00:00Z',
                        'to': '2023-02-09T15:59:59Z'
                    },
                    'mosaickingOrder': 'mostRecent',
                },
            }
        ]
    },
    'output': {
        'width': 1048,
        'height': 1048,
        'responses': [
            {
                'identifier': 'default',
                'format': {
                    'type': 'image/jpeg',
                }
            }
        ]
    },
    'evalscript': evalscript
}


def make_request(bbox):
    access_token = current_app.config["sentinel_token"]
    oauth = current_app.config["sentinel_oauth"]
    url, headers = setup_sentinel_headers(access_token)
    payload = get_request_json(bbox)
    response = oauth.request("POST", url, headers=headers, json = payload)
    if response.status_code != 200:
        oauth, access_token = setup_sentinel_token()
        current_app.config["sentinel_token"] = access_token
        current_app.config["sentinel_oauth"] = oauth
        url, headers = setup_sentinel_headers(access_token)
        response = oauth.request("POST", url, headers = headers, json = payload)
    return response

def get_sentinel_image(bbox):
    response = make_request(bbox)
    return np.array(Image.open(io.BytesIO(response.content)))