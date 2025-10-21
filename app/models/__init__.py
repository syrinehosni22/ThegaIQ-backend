from app import db
from app.models.user import User
from app.models.role import Role
from app.models.capability import Capability
from app.models.associations import role_capabilities  # add this line

__all__ = ["User", "Role", "Capability", "role_capabilities", "db"]
