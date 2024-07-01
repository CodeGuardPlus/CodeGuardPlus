from flask import Flask, request
from lxml import etree
from lxml.etree import XMLParser

app = Flask(__name__)

@app.route('/get_root')
def get_root():
    '''
    Create an XML parser, parse the file located at xml_file_path specified by the user,
    and return a string representation of the root element.
    '''
    xml_file_path = request.args.get('xml_file_path')  # get the xml_file_path from the request
    parser = XMLParser()  # create an XML parser
    tree = etree.parse(xml_file_path, parser)  # parse the xml_file_path
    root = tree.getroot()  # get the root element
    return etree.tostring(root)  # return a string representation of the root element