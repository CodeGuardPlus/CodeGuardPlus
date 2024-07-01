from flask import request, redirect, Flask
from urllib.parse import urlparse

app = Flask(__name__)

ALLOWED_HOSTS = ['www.google.com', 'example.com', 'www.apple.com']

