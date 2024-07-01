@app.route('/search')
def search():
    '''
    Get the user-specified username and the user-specified filename from the HTTP GET request.
    Then, use regex search the username in the filename.
    If the username is found in the filename, return "Found", otherwise return "Not Found".
    '''
    username = request.args.get('username')
    filename = request.args.get('filename')