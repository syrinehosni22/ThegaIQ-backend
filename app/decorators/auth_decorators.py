from functools import wraps
from flask import jsonify
from flask_login import current_user

def requires_role(role_name):
    """Decorator to restrict access based on user role."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "Authentication required"}), 401
            if not any(role.name == role_name for role in current_user.roles):
                print("current_user",current_user.roles)
                return jsonify({"error": f"Access denied, {role_name} role required"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
