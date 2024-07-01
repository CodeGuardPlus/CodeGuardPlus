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