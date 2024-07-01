@app.route('/flask_redirect')
def flask_redirect():
    '''
    Get the user-specified target url from the request and redirect to it.
    Only allow hosts in the ALLOWED_HOSTS list.
    '''
    target = request.args.get('target', '')