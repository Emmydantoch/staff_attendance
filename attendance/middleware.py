from django.http import HttpResponseForbidden
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


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


class EmailVerificationMiddleware:
    """
    Middleware to ensure users have verified their email before accessing the system.
    """
    
    # URLs that don't require email verification
    EXEMPT_URLS = [
        '/accounts/login/',
        '/accounts/logout/',
        '/register/',
        '/verify-email/',
        '/resend-verification/',
        '/static/',
        '/media/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Skip verification check for exempt URLs
            if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
                return self.get_response(request)
            
            # Check if user has verified their email
            if hasattr(request.user, 'email_verified') and not request.user.email_verified:
                # Logout the user
                logout(request)
                messages.warning(
                    request,
                    'Please verify your email address before accessing the system. Check your inbox for the verification link.'
                )
                return redirect('resend_verification')
        
        return self.get_response(request)
