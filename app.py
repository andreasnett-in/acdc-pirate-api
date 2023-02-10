from flask import *
import json
from get_coords import get_coords
from model.entry import predict

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    print("API Status ok")
    return "API Status ok"


@app.route("/do-predictions", methods=["GET"])
def do_predictions():
    bboxes = get_coords()
    results = []
    for bbox in bboxes:
        results.append((bbox), predict(bbox))
    # store results
    return "Done"