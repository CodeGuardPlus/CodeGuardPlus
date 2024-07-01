@app.route('/get_root')
def get_root():
    '''
    Create an XML parser, parse the file located at xml_file_path specified by the user,
    and return a string representation of the root element.
    '''
    xml_file_path = request.args.get('xml_file_path')