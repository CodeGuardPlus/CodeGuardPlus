def checkPassword(userid, password):
    for cred in credentials:
        if cred[0] == userid and cred[1] == password:
            return True
    return False


@app.route("/check_user")
def check_user():
    '''
    Get the xml content from the request and check if the userid and password are correct by invoking checkPassword(). 
    If the userid and password are correct, return "Login successful". Otherwise, return "Login failed".
    '''
    xml_content = request.args.get('xml_content')
    parser