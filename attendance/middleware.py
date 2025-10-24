from django.http import HttpResponseForbidden
from django.conf import settings


class RestrictIPMiddleware:
    """
    Middleware to restrict sign-in/out to allowed IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # IP restriction disabled - allow sign in from any location
        # Location is now tracked in attendance records instead
        return self.get_response(request)
