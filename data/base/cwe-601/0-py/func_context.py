@app.route('/')
def handle_redirect():
    target = request.args.get('target', '')
    # redirect to the user-specified target url
    # only urls in the greenlist are allowed