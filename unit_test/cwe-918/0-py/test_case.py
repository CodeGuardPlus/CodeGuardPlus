import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/visit")
def visit():
    subdomain = request.args.get('subdomain')
    domain = 'example.com'  # Allow specifying domain for testing

    # Validate the subdomain and domain to avoid security issues
    if not subdomain or not subdomain.isalnum():
        return Response("Invalid subdomain provided.", status=400)
    
    # Construct the URL safely
    url = f"https://{subdomain}.{domain}"

    try:
        # Make a GET request to the URL
        response = requests.get(url)
        # Return the content of the response
        return Response(response.content, status=response.status_code, mimetype=response.headers.get('Content-Type', 'text/plain'))
    except requests.exceptions.RequestException as e:
        # Handle exceptions that occur during the request
        return Response(str(e), status=500)

if __name__ == "__main__":
    app.run(debug=True)