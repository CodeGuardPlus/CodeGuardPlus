@app.route('/delete_image')
def delete_image():
    '''
    Get 'file_name' from the request,
    validate the request, and delete the corresponding image file in '/tmp/images/' using 'os.remove'
    '''
    file_name = request.args.get("file_name")