from django.http import HttpResponseForbidden


class RestrictIPMiddleware:
    """
    Middleware to restrict sign-in/out to allowed IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict for sign-in/out views
        if request.path.startswith("/sign-in-out/"):
            allowed_ips = [
                "192.168.1.100",  # Replace with your allowed system's IPs
                "192.168.1.101",
                "192.168.1.102",
            ]
            ip = request.META.get("REMOTE_ADDR")
            if ip not in allowed_ips:
                return HttpResponseForbidden(
                    "Sign-in/out allowed only from the office systems."
                )
        return self.get_response(request)
