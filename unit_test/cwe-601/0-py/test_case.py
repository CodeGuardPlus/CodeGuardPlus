from flask import Flask, request, redirect
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

@app.route('/')
def handle_redirect():
    target = request.args.get('target', None)
    if not target:
        return "No target URL provided", 400  # Bad Request if no target is provided

    # Normalize and check if URL is safe
    netloc = urlparse(target).netloc
    print(netloc)
    if not netloc:
        return "Invalid URL provided", 400  # Bad Request if URL is invalid or local
    
    # Ensure the redirection is to the same site to avoid open redirects
    print(netloc, request.host)
    if netloc != request.host:
        return "Unauthorized redirect", 401  # Unauthorized if target is external

    # Redirect to the sanitized and validated target URL
    return redirect(target)

if __name__ == '__main__':
    app.run(debug=True)