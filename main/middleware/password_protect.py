from django.shortcuts import redirect
from django.urls import reverse

class PasswordProtectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to the password page and static files
        allowed_paths = [reverse('password'), '/static/', '/admin/login/']
        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)
        # Check session for authentication
        if not request.session.get('authenticated', False):
            return redirect('password')
        return self.get_response(request)
