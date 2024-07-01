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
    tree = ET.parse('/tmp/users.xml')
    root = tree.getroot()
    username = request.args.get('username')