from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

ALLOWED_HOSTS = ['www.google.com', 'example.com', 'www.apple.com']

