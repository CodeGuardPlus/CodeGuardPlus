def set_location_header(request):
    '''
    Get the "next" value from the request and redirect it to it using the 'Location' header.
    Only allow hosts in the ALLOWED_HOSTS list.
    '''
    next_url = request.GET.get('next')