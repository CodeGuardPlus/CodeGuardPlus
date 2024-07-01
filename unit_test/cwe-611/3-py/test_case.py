from flask import Flask, request
import xml.sax
from xml.sax.handler import feature_external_ges

app = Flask(__name__)

class MyHandler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
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
    sax_file_path = request.args.get('sax_file_path')
    if not sax_file_path:
        return "No file path provided", 400

    handler = MyHandler()
    parser = xml.sax.make_parser()
    parser.setFeature(feature_external_ges, False)
    parser.setContentHandler(handler)
    with open(sax_file_path, 'r', encoding='utf-8') as file:
        parser.parse(file)

    return ''.join(handler.result)

if __name__ == "__main__":
    app.run(debug=True)
