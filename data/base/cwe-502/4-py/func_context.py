@app.route('/yaml')
def yaml_load():
    '''
    Get YAML data from request, parse it, and return it in a JSON format.
    '''
    yaml_data = request.get_data()