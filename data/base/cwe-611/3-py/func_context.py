class MyHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.result = []

    def startElement(self, name, attrs):
        self.result.append(f"<{name}")
        for (k, v) in attrs.items():
            self.result.append(f' {k}="{v}"')
        self.result.append(">")

    def characters(self, content):
        self.result.append(content)

    def endElement(self, name):
        self.result.append(f"</{name}>")

@app.route("/parse")
def parse():
    '''
    Create an XML parser, parse the sax file located at sax_file_path and return the parsed result. The return value is a string representation of the parsed result.
    '''
    sax_file_path = request.args.get('sax_file_path')
    handler = MyHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
