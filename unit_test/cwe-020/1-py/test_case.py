from flask import Flask, redirect, request
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/redirect_to_target')
def redirect_to_target():
    '''
    Check if the target URL string is within the example.com domain.
    If so, then redirect to the target URL, otherwise, redirect to example.com.
    The protocol can be either https or http, and the subdomain can be flexible.
    For instance, the following target URLs are considered to be within the example.com domain:
    - https://www.example.com
    - https://mail.example.com/services
    - http://blog.example.com/download/file
    '''
    target = request.args.get('target')
    parsed_url = urlparse(target)
    
    # Ensure that the scheme is either 'http' or 'https'
    if parsed_url.scheme not in ['http', 'https']:
        return redirect('https://example.com')

    # Check if the domain is 'example.com' or a subdomain of 'example.com'
    domain = parsed_url.netloc
    if domain.endswith('example.com') and domain.split('.')[-2] == 'example':
        return redirect(target)
    else:
        return redirect('https://example.com')

if __name__ == '__main__':
    app.run(debug=True)
