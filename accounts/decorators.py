from django.shortcuts import redirect
from functools import wraps


def _landing_for(role):
    if role == 'kasir':
        return 'buat_transaksi'
    return 'dashboard'


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                role = request.user.profile.role
            except AttributeError:
                return redirect('login')

            if role not in allowed_roles:
                return redirect(_landing_for(role))

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
