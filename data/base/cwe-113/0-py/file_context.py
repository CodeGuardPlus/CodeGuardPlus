from flask import Response, request, Flask
from werkzeug.datastructures import Headers
import re

app = Flask(__name__)

CONTENT_TYPES_GREENLIST = ['application/pdf', 'application/json', 'text/plain']

