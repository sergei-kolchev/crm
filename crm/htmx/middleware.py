from htmx.http import HtmxData


class HtmxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.htmx = HtmxData(request)
        return self.get_response(request)
