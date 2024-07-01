from flask import Flask, request, Response
import defusedxml.ElementTree as ET

app = Flask(__name__)

@app.post("/parse_xml")
def parse_xml():
    # Retrieve XML from the request body
    xml_data = request.args.get('xml_src')
    print(xml_data)

    if not xml_data:
        return "No XML data provided", 400  # Return 400 Bad Request if no data is provided

    try:
        # Parse the XML data safely
        root = ET.fromstring(xml_data)

        # Convert XML structure to a string representation
        result_string = ET.tostring(root, encoding='unicode')

        # Return the result string
        return Response(result_string, mimetype='text/plain')

    except ET.ParseError:
        return "Invalid XML provided", 400  # Return 400 Bad Request if XML is malformed

    except Exception as e:
        # Generic error handling to catch unforeseen errors
        return f"An error occurred: {str(e)}", 500  # Return 500 Internal Server Error for any other exceptions

if __name__ == '__main__':
    app.run(debug=True)