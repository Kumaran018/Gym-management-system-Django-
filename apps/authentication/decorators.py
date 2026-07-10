from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for views that checks if the logged-in user has one of the allowed roles.
    If unauthorized, they are redirected to their appropriate home dashboard.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            
            user = request.user
            if user.is_superuser or user.role == 'admin' or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # Redirect to their respective dashboards
            if user.role == 'admin':
                return redirect('dashboard:admin_home')
            elif user.role == 'receptionist':
                return redirect('dashboard:reception_home')
            elif user.role == 'trainer':
                return redirect('dashboard:trainer_home')
            elif user.role == 'member':
                return redirect('dashboard:member_home')
            
            return redirect('authentication:login')
        return _wrapped_view
    return decorator
