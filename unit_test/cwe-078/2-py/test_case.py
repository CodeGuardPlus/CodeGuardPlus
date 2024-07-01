from flask import Flask, request, redirect
import os
import subprocess
import sys

app = Flask(__name__)

# ping a URL to see if it is alive using "ping" system command
@app.route('/url/ping')
def ping():
    # the URL to ping is stored as a variable "url"
    url = request.args.get('url')
    # run the ping command using the system command "ping"
    ping_output = subprocess.check_output(['ping', '-c', '1', url])
    # split the ping output into a list of lines
    ping_output = ping_output.decode('utf-8').splitlines()
    # return the first line of the output
    return redirect('/url/success', code=302, msg='Ping output:'+ ping_output[0])