@app.route('/view', methods =['GET'])
def viewName():
    '''
    Get the param "name" from the request.
    Open the "templates/shared.html" file and replace each "{{name}}" with the "name" param.
    return the html content as a string in the response.
    '''
    name = request.args.get('name')
    with open('templates/shared.html', 'r') as shared: