from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


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
                messages.error(request, 'Akun kamu belum punya profil/role. Hubungi admin.')
                return redirect('dashboard')

            if role not in allowed_roles:
                messages.error(request, 'Kamu tidak punya akses ke halaman ini.')
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator