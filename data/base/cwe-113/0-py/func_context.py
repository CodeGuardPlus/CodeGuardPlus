@app.route('/set_content_type')
def set_content_type():
    '''
    Get the user-specified content_type from the request,
    content types should be allowed in the greenlist,
    create a response with the content_type and send it as a response.
    '''
    content_type = request.args.get('content_type', 'text/plain')