from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.has_permission(permission):
                # If user doesn't have the required permission, handle the case accordingly
                # For example, redirect them to a different route or return an error message
                return redirect(url_for('no_permission'))  # Redirect to a route for handling permission errors
            return func(*args, **kwargs)
        return wrapper
    return decorator
