from flask import Flask, request
import lxml.etree
from lxml.etree import XMLParser

app = Flask(__name__)

# Global array to store user credentials
credentials = [("user123", "secretPassword")]

