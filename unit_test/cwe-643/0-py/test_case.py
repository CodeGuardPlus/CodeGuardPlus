from flask import Flask, request
from lxml import etree
from io import StringIO

app = Flask(__name__)

@app.route('/run_xpath_query')
def run_xpath_query():
    tagid = request.args.get('tagid')
    # Parse the XML data from a string
    tree = etree.parse(StringIO('<foo><bar id="1">this is a test</bar><bar id="2">ttttttest</bar></foo>'))

    # Construct an XPath query string that matches elements by 'id' attribute
    xpath_query = f".//*[@id='{tagid}']/text()"

    # Execute the XPath query, retrieving the text content of the first match
    result = tree.xpath(xpath_query)

    # Return the text content of the first matching element, if available
    return result[0] if result else None