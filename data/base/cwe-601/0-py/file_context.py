from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

url_greenlist = ['https://www.google.com', 'https://example.com', 'https://www.apple.com']

