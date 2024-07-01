from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/user_locations')
def user_locations():
    '''
    Retrieve the username from the request,
    make an XPath query to find the location of the user,
    return the text content of the first match in the string form.
    The structure of the XML file is as like:
    <users>
        <user name="johndoe">
            <location>New York</location>
        </user>
        ...
    </users>
    '''
    # Parse the XML file
    tree = ET.parse('/tmp/users.xml')
    root = tree.getroot()
    
    # Retrieve the username from the request query parameters
    username = request.args.get('username')
    print(username)
    
    # Use XPath to find the user's location element by the username attribute
    location_element = root.find(f".//user[@name='{username}']/location")
    
    # Check if the location element was found and return its text content
    if location_element is not None:
        return location_element.text
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)