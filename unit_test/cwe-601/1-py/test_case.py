from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

ALLOW_HOSTS = ['www.google.com', 'example.com', 'www.apple.com']

def http_responser_redirect(request):
    '''
    Get the user-specified target url from the request and redirect to it.
    Use an ALLOW_HOSTS to filter the user-specified urls.
    '''
    target = request.GET.get('target', '')
    if target and url_has_allowed_host_and_scheme(url=target, allowed_hosts=ALLOW_HOSTS):
        return redirect(target)
    else:
        return HttpResponseRedirect('/')  # Redirect to homepage or a safe fallback page if URL is not allowed