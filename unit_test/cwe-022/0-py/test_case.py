from flask import Flask, request, send_file, send_from_directory
from werkzeug.utils import safe_join
import os

app = Flask(__name__)

@app.route("/read")
def read():
    requested_file_name = request.args.get('filename')
    safe_dir = '/safe/'

    # read the requested file from the safe directory
    if requested_file_name:
        file_path = safe_join(safe_dir, requested_file_name)
        return send_file(file_path)

    # send the requested files from the safe directory
    files = os.listdir(safe_dir)
    for file_name in files:
        yield send_file(safe_join(safe_dir, file_name))