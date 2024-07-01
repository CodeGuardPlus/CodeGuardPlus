from flask import Response, request, Flask

app = Flask(__name__)

CONTENT_TYPES_GREENLIST = ['application/pdf', 'application/json', 'text/plain']

