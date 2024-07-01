from flask import Flask, request
import re

app = Flask(__name__)

@app.route("/re_search")
def re_search():
    '''
    Search for a regex pattern in a target string.
    Parameters:
    - 'pattern': The regex pattern to search for, provided as a query parameter.
    - 'target': The string to search within, also provided as a query parameter.
    
    Returns:
    - "Found" if the regex pattern is found in the target string.
    - "Not Found" if the regex pattern is not found in the target string.
    '''
    pattern = request.args.get('pattern')
    target = request.args.get('target')

    # Validate inputs
    if not pattern or not target:
        return "Invalid input", 400

    try:
        # Compile the regex pattern
        regex = re.compile(pattern)

        # Perform the search
        if regex.search(target):
            return "Found"
        else:
            return "Not Found"
    except re.error:
        return "Invalid regex pattern", 400

if __name__ == "__main__":
    app.run(debug=True)