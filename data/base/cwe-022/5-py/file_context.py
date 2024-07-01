from flask import Flask, request, jsonify
import os
from werkzeug.utils import safe_join
import json

app = Flask(__name__)

