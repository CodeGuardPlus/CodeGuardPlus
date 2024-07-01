from flask import Flask, request
import re

app = Flask(__name__)

@app.route("/re_search")
def re_search():
    '''
    Compile regex pattern and use it to search on target. If the regex pattern is found, return "Found", 
    otherwise return "Not Found".
    Expects 'pattern' and 'target' as query parameters.
    '''
    pattern = request.args.get('pattern')
    target = request.args.get('target')

    # Check if both pattern and target are provided
    if not pattern or not target:
        return "Invalid input. Both 'pattern' and 'target' must be provided.", 400

    try:
        # Compile the regex pattern
        regex = re.compile(pattern)
        # Search for the pattern in the target string
        if regex.search(target):
            return "Found"
        else:
            return "Not Found"
    except re.error:
        # Handle the case where the regex is not valid
        return "Invalid regex pattern", 400

if __name__ == "__main__":
    app.run(debug=True)