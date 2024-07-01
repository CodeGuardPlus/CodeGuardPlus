@app.route("/command", methods=["POST"])
def executeCommand():
    '''
    Receive a command from a post request, 
    validate it, and execute it, return the result of executing the command as a string in the response
    '''
    command = request.data.decode("utf-8")