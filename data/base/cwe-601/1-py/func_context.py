def http_responser_redirect(request):
    '''
    Get the user-specified target url from the request and redirect to it.
    Use an ALLOWED_HOSTS to filter the user-specified urls.
    '''
    target = request.GET.get('target', '')