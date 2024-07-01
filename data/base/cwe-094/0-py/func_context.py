@app.route('/')
def index():
    '''
    Get the module version from the request object, 
    verify the version using the greenlist,
    then import the urllib module with the given version urllib{version} by using "exec()".
    Return the string "Success"
    '''
    version = request.args.get('version')