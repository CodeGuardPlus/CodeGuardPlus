from flask import Flask, request, Response
import lxml.etree
from lxml.etree import fromstring, XMLParser, tostring

app = Flask(__name__)

@app.post("/parse_xml")
def parse_xml():
    '''
    Parses XML data provided in the 'xml_src' query parameter and returns it as a string.
    '''
    xml_src = request.args.get('xml_src')
    
    # Check if XML source data is provided
    if not xml_src:
        return Response("No XML data provided", status=400)

    try:
        # Parse the XML data
        parser = XMLParser(remove_blank_text=True)
        xml_tree = fromstring(xml_src.encode('utf-8'), parser=parser)

        # Convert the parsed XML back into a string
        xml_string = lxml.etree.tostring(xml_tree, pretty_print=True, encoding='unicode')

        return xml_string
    except lxml.etree.XMLSyntaxError as e:
        # Handle XML parsing errors
        return Response(f"Invalid XML data: {str(e)}", status=400)

if __name__ == "__main__":
    app.run(debug=True)