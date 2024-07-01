import hashlib
from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/index')
def index():
    password = request.args.get('password')
    response = make_response()
    # securely set the sensitive password in cookie and return the response
    response.set_cookie('password', password, httponly=True, secure=True)
    return response