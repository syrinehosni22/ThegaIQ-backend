from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.models.user import User
from app.models.role import Role
from app.decorators.auth_decorators import requires_role
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)

# -------------------------
# GET all users (Admin only)
# -------------------------
@user_bp.route('/all', methods=['GET'])
@login_required
@requires_role('admin')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# -------------------------
# GET single user by ID
# -------------------------
@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@requires_role('admin')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# -------------------------
# CREATE user
# -------------------------
@user_bp.route('/new', methods=['POST'])
@login_required
@requires_role('admin')
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_names = data.get('roles', [])  # optional list of roles

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User with same username or email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)

    # Assign roles if provided
    if role_names:
        roles = Role.query.filter(Role.name.in_(role_names)).all()
        new_user.roles = roles

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created", "user": new_user.to_dict()}), 201


# -------------------------
# UPDATE user
# -------------------------
@user_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
@requires_role('admin')
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    # If password provided → hash it
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])

    # Update roles if provided
    if 'roles' in data:
        roles = Role.query.filter(Role.name.in_(data['roles'])).all()
        user.roles = roles

    db.session.commit()
    return jsonify({"message": "User updated", "user": user.to_dict()}), 200


# -------------------------
# DELETE user
# -------------------------
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@requires_role('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
