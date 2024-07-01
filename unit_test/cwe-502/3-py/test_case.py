from flask import Flask, request, jsonify
import pickle
import json
import base64


app = Flask(__name__)

@app.route('/get_data', methods=['POST'])
def get_deserialized_data():
    # read serialized data, return deserialized data in a json format
    serialized_data = request.data # get serialized data from request
    data = pickle.loads(serialized_data) # deserialize data
    return jsonify(data) # return data in a json format