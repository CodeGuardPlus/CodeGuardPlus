@app.route('/load')
def load():
    '''
    Use the filename variable to open a file, 
    load its contents into a variable with yaml, and return it in the json format
    '''
    filename = request.args.get('filename', None)