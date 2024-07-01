from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

