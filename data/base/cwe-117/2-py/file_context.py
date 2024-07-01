from flask import request, Flask
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

