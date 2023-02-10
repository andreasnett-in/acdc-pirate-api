from flask import Flask, request
from get_coords import get_coords, normalize_ais_coords
from ais import setup_ais_token, get_ais_data
from sentinel import setup_sentinel_token
from model.entry import predict
from random import randint

app = Flask(__name__)
def setup_config():
    app.config["ais_token"] = setup_ais_token()
    sentinel_oauth, sentinel_token = setup_sentinel_token()
    app.config["sentinel_token"] = sentinel_token
    app.config["sentinel_oauth"] = sentinel_oauth
setup_config()

@app.route("/", methods=["GET"])
def health_check():
    print("API Status ok")
    return "API Status ok"


@app.route("/random-coord", methods=["GET"])
def get_random_coord():
    bboxes = get_coords()
    rand = randint(0, len(bboxes)-1)
    entry = [coord for coord in bboxes[rand]]
    return normalize_ais_coords(entry)

@app.route("/get-ais-data", methods=["POST"])
def get_ais_data_endpoint():
    coords = request.get_json()["coords"]
    if not len(coords) == 5:
        return "Bad formatting"
    return get_ais_data(coords)


@app.route("/do-predictions", methods=["GET"])
def do_predictions():
    bboxes = get_coords()
    results = []
    for bbox in bboxes:
        results.append(([coord for coord in bbox].append(bbox[0])), predict(bbox))
    # store results
    return "Done"