from functools import wraps
from flask import jsonify
from flask_login import current_user

def requires_capability(capability_name):
    """Decorator to restrict access based on a specific capability, including child roles."""
    
    def gather_capabilities(role, collected=None):
        """Recursively gather capabilities from a role and its children."""
        if collected is None:
            collected = set()
        # Add capabilities of this role
        collected.update({cap.name for cap in role.capabilities})
        # Recursively add capabilities from children roles
        for child in role.children:
            gather_capabilities(child, collected)
        return collected

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "Authentication required"}), 401

            # Gather capabilities from all roles and their children
            user_capabilities = set()
            for role in current_user.roles:
                user_capabilities.update(gather_capabilities(role))

            if capability_name not in user_capabilities:
                print(f"You don't have the '{capability_name}' capability")
                return jsonify({"error": f"Access denied, '{capability_name}' capability required"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
