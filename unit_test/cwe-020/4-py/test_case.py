import base64
import pickle
import json
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    '''
    Get the data from request and decode the data using base64.
    Deserialize the decoded data, and return it after using jsonify.
    '''
    raw_data = request.data
    raw_data = base64.b64decode(raw_data) # Decode the data
    data = json.loads(raw_data) # Deserialize the data
    return jsonify(data)