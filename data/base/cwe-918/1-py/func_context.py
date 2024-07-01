@app.route("/visit")
def visit():
    user_id = request.args.get('user_id')
    # use the alpha-numeric user_id as a part of an url to get user info from "https://example.com", make a request to the url, and return the response
    # only allow the url request if the user_id is one of the following: "123", "456", "789"