from flask import Flask, request, jsonify
from lxml import etree
from lxml.etree import XMLParser

app = Flask(__name__)

