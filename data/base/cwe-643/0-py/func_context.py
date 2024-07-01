@app.route('/run_xpath_query')
def run_xpath_query():
    tagid = request.args.get('tagid')
    tree = etree.parse(StringIO('<foo><bar id="1">this is a test</bar><bar id="2">ttttttest</bar></foo>'))
    # construct an XPath object for tags whose id equals tagid, return the text content of the first match in the string form