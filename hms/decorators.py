from django.http import HttpResponseForbidden

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_groups = request.user.groups.values_list('name', flat=True)

            if any(group in allowed_roles for group in user_groups):
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("You do not have permission.")

        return wrapper
    return decorator
