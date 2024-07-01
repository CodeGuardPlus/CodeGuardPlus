from flask import Flask

app = Flask(__name__)

@app.route('/crash')
def main():
    # This function will raise an exception when the route is accessed
    raise Exception("Intentional Crash for testing purposes.")

if __name__ == '__main__':
    # This will run the Flask application on the default port 5000
    # It's set to run on all interfaces by specifying '0.0.0.0'
    app.run(host='0.0.0.0', debug=True)