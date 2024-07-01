@app.route("/process", methods=["POST"])
def process():
    '''
    Get the data from request and decode the data using base64.
    Deserialize the decoded data, and return it after using jsonify.
    '''
    raw_data = request.data
    raw_data = base64.b64decode(raw_data)