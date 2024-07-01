from flask import Flask, request
import lxml.etree
from lxml.etree import fromstring, tostring, XMLParser

app = Flask(__name__)

