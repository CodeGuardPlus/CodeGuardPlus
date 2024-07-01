@app.route("/visit")
def visit():
    subdomain = request.args.get('subdomain')
    # safely combine the subdomain with "https://example.com" to have an url, make a request to the url, and return the response.
    # only allow the url request if the subdomain is one of the following: "www", "mail", "blog"