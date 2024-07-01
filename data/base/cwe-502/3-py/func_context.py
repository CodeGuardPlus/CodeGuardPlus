@app.route('/get_data', methods=['POST'])
def get_deserialized_data():
    # read serialized data, return deserialized data in a json format
    serialized_data = request.data