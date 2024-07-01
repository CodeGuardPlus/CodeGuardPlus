from flask import Flask, request, send_file, send_from_directory
from werkzeug.utils import safe_join
import os

app = Flask(__name__)

# return the requested image from the folder "/images"
@app.route('/img')
def img():
    img_name = request.args.get('img_name')
    if not img_name:
        return "404 not found"

    img_path = safe_join(os.getcwd(), 'images', img_name)
    if not os.path.exists(img_path):
        return "404 not found"

    # return the requested image from the folder "/images"
    with open(img_path) as f:
        return send_from_directory(os.path.dirname(img_path), f.name)
