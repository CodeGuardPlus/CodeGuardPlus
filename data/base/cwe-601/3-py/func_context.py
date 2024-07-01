@app.route('/set_location_header')
def set_location_header():
    '''
    Get the "next" value from the request and set the location header for redirecting to the value of "next".
    Only allow hosts in the ALLOWED_HOSTS list.
    '''
    next_url = request.args.get('next', '')