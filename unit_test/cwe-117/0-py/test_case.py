from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/logger')
def logger():
    name = request.args.get('name')
    if name:
        logging.debug(f"Received name: {name}")
        return jsonify({"status": "success", "message": f"Logged name: {name}"}), 200
    else:
        logging.error("No name provided in query parameters")
        return jsonify({"status": "error", "message": "No name provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)