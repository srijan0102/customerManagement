from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


def permission_grated(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_fuction(request, *args, **kwargs):
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    if group.name in allowed_roles:
                        return view_function(request, *args, **kwargs)
                    else:
                        return PermissionDenied('Access Denied')
            else:
                return PermissionDenied('Access Denied')
        return wrapper_fuction
    return decorator
    

def admin_extended_permission(view_func):
    def wrapper_fuction(request, *args, **kwargs):
        if request.user.groups.exists():
            groups = request.user.groups.all()
            for group in groups:
                if group.name == 'CUSTOMER':
                    return redirect(reverse('accounts:customer_profile'))
                if group.name == 'ADMIN':
                    return view_func(request, *args, **kwargs)
        else:
            raise ImproperlyConfigured('No Group Exist')
    return wrapper_fuction