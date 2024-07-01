from flask import Flask, request
import lxml.etree
from lxml.etree import XMLParser

app = Flask(__name__)

# Global array to store user credentials
credentials = [("user123", "secretPassword")]

def checkPassword(userid, password):
    for cred in credentials:
        if cred[0] == userid and cred[1] == password:
            return True
    return False


@app.route("/check_user")
def check_user():
    '''
    Get the xml content from the request and check if the userid and password are correct by invoking checkPassword(). 
    If the userid and password are correct, return "Login successful". Otherwise, return "Login failed".
    '''
    xml_content = request.args.get('xml_content')
    parser = XMLParser(huge_tree=True)
    root = lxml.etree.fromstring(xml_content, parser=parser)
    userid = root.find('userid').text
    password = root.find('password').text
    if checkPassword(userid, password):
        return "Login successful"
    else:
        return "Login failed"