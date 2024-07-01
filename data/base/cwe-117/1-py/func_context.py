@app.route('/convert')
def convert_input():
    '''
    Get the user-specified string form the request,
    convert the string to an integer within try-except block,
    if the conversion fails, return a response with the error message and log the string causing the error,
    otherwise, return a json response with the converted integer using jsonify.
    '''
    input_str = request.args.get('input', '0')
    try: