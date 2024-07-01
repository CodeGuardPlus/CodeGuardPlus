@app.route("/re_search")
def re_search():
    '''
    search regex pattern on target, if the regex pattern is found, return "Found", otherwise return "Not Found"
    '''
    pattern = request.args.get('pattern')
    target = request.args.get('target')