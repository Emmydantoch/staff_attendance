from django.http import HttpResponseForbidden
from django.conf import settings


class RestrictIPMiddleware:
    """
    Middleware to restrict sign-in/out to allowed IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_prefixes = (
            "/sign-in-out/",
            "/barcode-authenticate/",
            "/barcode-scan/",
        )
        if any(request.path.startswith(p) for p in protected_prefixes):
            allowed_ips = getattr(settings, "ALLOWED_SIGNIN_IPS", ["172.16.20.10"]) or [
                "127.0.0.1",
                "::1",
            ]
            xff = request.META.get("HTTP_X_FORWARDED_FOR")
            if xff:
                ip = xff.split(",")[0].strip()
            else:
                ip = request.META.get("REMOTE_ADDR")
            if ip not in allowed_ips:
                return HttpResponseForbidden("Sign-in/out allowed only from the office systems.")
        return self.get_response(request)
