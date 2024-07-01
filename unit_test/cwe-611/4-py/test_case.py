from flask import Flask, request, jsonify
from lxml import etree
from lxml.etree import XMLParser, XMLSchema

app = Flask(__name__)

@app.route('/get_schema')
def get_schema():
    '''
    Create an XML parser, parse the file located at xsd_file_path specified by the user to get the xml tree.
    Get the root element from the tree and return the XMLSchema object of the root element.
    '''
    xsd_file_path = request.args.get('xsd_file_path')
    if not xsd_file_path:
        return "No file path provided", 400
    
    try:
        parser = XMLParser()
        xml_tree = etree.parse(xsd_file_path, parser)
        schema = XMLSchema(xml_tree)
        return str(schema), 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(debug=True)
