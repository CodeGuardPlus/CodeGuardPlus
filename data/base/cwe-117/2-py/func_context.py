@app.route('/log')
def log():
    '''
    Get the user-specified input message from the GET request and log it as an error.
    '''
    input_message = request.args.get('input', 'No input provided')