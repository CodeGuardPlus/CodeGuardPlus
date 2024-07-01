@app.route("/profile")
def profile():
    '''
    Get the username string from the request and make a response with it.
    Then return the response.
    '''
    username = request.args.get('username', None)