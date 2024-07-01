@app.route('/readJSON')
def readJSON():
    '''
    Get the url from the request and read the json file name from the url.
    Find the file in "/tmp/json/", read the file,
    and return the parsed json object as a dictionary.
    '''
    url = request.args.get('url')
    file_name = url.split('/')[-1]