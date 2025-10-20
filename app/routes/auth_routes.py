from flask import Blueprint, jsonify, request
from app.services.auth_service import register_user, login_user_service, logout_user_service

auth_bp = Blueprint('auth_bp', __name__)


# 🧩 Test route to verify Flask setup
@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Auth route working successfully!"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password')
    user, error = register_user(username, email, password)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(user.to_dict()), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    user, error = login_user_service(email, password)
    if error:
        return jsonify({"error": error}), 401
    return jsonify({"message": f"Welcome {user.username}!"}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user_service()
    return jsonify({"message": "Logged out"}), 200
