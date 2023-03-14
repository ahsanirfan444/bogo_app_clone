from django.http import HttpResponsePermanentRedirect


class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(':')[0]
        
        if not "https" in request.build_absolute_uri() and host == "dev-portal.huburway.com":
            return HttpResponsePermanentRedirect('https://dev-portal.huburway.com/'+request.path)
        elif not "https" in request.build_absolute_uri() and host == "portal.huburway.com":
            return HttpResponsePermanentRedirect('https://portal.huburway.com/'+request.path)
        else:
            return self.get_response(request)
        