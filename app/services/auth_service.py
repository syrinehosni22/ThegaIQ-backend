from app import db
from app.models.user import User
from app.models.role import Role
from app.utils.security import hash_password, verify_password
from flask_login import login_user, logout_user

def register_user(username, email, password):
    """Create a new user and save to the database."""
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"

    hashed_password = hash_password(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    print("role in session",user.roles)
    return user, None


def login_user_service(email, password):
    """Authenticate a user."""
    user = User.query.filter_by(email=email).first()
    if user and verify_password(password, user.password_hash):
        login_user(user)
        return user, None
    return None, "Invalid credentials"


def logout_user_service():
    """Logout the current user."""
    logout_user()
    return {"message": "Logged out successfully"}
