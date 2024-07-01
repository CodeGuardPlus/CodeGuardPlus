from flask import Flask, request, Response
from lxml import etree
from lxml.etree import XMLParser
import os

app = Flask(__name__)

