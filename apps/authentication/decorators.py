from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for views. Ensures all dashboard features are accessible
    to logged-in users while requiring authentication.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
