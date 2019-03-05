from functools import wraps


def validate_staff():
    def decorator(func):
        @wraps(func)
        def inner(request,is_staff, *args, **kwargs):



            return func(request, *args, **kwargs)
        return inner
    return decorator