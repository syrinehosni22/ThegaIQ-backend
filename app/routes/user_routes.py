from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.user import User
from app.models.role import Role
from app.decorators.auth_decorators import requires_role
from app.decorators.capability_role import requires_capability
from werkzeug.security import generate_password_hash


user_bp = Blueprint('user_bp', __name__, template_folder='templates/users')


def wants_json_response():
    """Helper: detect if the request wants JSON (API)."""
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html'] \
        or request.args.get('format') == 'json'


# ✅ GET all users
@user_bp.route('/all', methods=['GET'])
@login_required
@requires_role('Administrator')
@requires_capability(('view_all_users'))
def get_users():
    users = User.query.all()

    if wants_json_response():
        return jsonify([user.to_dict() for user in users]), 200

    return render_template('list.html', users=users)


# ✅ GET single user by ID
@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@requires_role('Administrator')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        if wants_json_response():
            return jsonify({"error": "User not found"}), 404
        flash("User not found", "danger")
        return redirect(url_for('user_bp.get_users'))

    if wants_json_response():
        return jsonify(user.to_dict()), 200

    return render_template('details.html', user=user)


# ✅ CREATE user
@user_bp.route('/new', methods=['GET', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_add_users'))
def create_user():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_names = data.getlist('roles') if not request.is_json else data.get('roles', [])

        if not all([username, email, password]):
            msg = {"error": "Missing required fields"}
            if wants_json_response():
                return jsonify(msg), 400
            flash("All fields are required!", "danger")
            return redirect(url_for('user_bp.create_user'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            msg = {"error": "User with same username or email already exists"}
            if wants_json_response():
                return jsonify(msg), 400
            flash("User already exists!", "warning")
            return redirect(url_for('user_bp.get_users'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)

        if role_names:
            roles = Role.query.filter(Role.name.in_(role_names)).all()
            new_user.roles = roles

        db.session.add(new_user)
        db.session.commit()

        if wants_json_response():
            return jsonify({"message": "User created", "user": new_user.to_dict()}), 201

        flash("User created successfully!", "success")
        return redirect(url_for('user_bp.get_users'))

    roles = Role.query.all()
    return render_template('create.html', roles=roles)


# ✅ UPDATE user
@user_bp.route('/<int:user_id>/edit', methods=['GET', 'PUT', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_modify_users'))
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        if wants_json_response():
            return jsonify({"error": "User not found"}), 404
        flash("User not found", "danger")
        return redirect(url_for('user_bp.get_users'))

    if request.method in ['PUT', 'POST']:
        data = request.get_json() if request.is_json else request.form
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])

        if 'roles' in data:
            roles = Role.query.filter(Role.name.in_(data['roles'])).all()
            user.roles = roles

        db.session.commit()

        if wants_json_response():
            return jsonify({"message": "User updated", "user": user.to_dict()}), 200

        flash("User updated successfully!", "success")
        return redirect(url_for('user_bp.get_users'))

    roles = Role.query.all()
    return render_template('edit.html', user=user, roles=roles)


# ✅ DELETE user
@user_bp.route('/<int:user_id>/delete', methods=['DELETE', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_delete_users'))
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        if wants_json_response():
            return jsonify({"error": "User not found"}), 404
        flash("User not found", "danger")
        return redirect(url_for('user_bp.get_users'))

    db.session.delete(user)
    db.session.commit()

    if wants_json_response():
        return jsonify({"message": "User deleted"}), 200

    flash("User deleted successfully!", "success")
    return redirect(url_for('user_bp.get_users'))
