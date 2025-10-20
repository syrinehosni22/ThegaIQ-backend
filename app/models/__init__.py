from app import db
from app.models.user import User
from app.models.role import Role

# Optional: import other models later
# from app.models.post import Post
# from app.models.comment import Comment

__all__ = ["User", "Role", "db"]
