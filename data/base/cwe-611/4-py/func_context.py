@app.route('/get_schema')
def get_schema():
    '''
    Create an XML parser, parse the file located at xsd_file_path specified by the user to get the xml tree.
    Get the root element from the tree and return the XMLSchema of the root element in a string format like str(schema).
    '''
    xsd_file_path = request.args.get('xsd_file_path')