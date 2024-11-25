from django.http import HttpResponse


class IgnoreInvalidRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            if "no URI read" in str(e):
                return HttpResponse("Invalid request", status=400)
            raise
