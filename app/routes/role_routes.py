from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.services.role_service import (
    create_role_service,
    get_all_roles_service,
    update_role_service,
    delete_role_service
)
from app.decorators.auth_decorators import requires_role

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/roles', methods=['GET'])
@login_required
@requires_role('admin')
def get_roles():
    roles = get_all_roles_service()
    return jsonify([role.to_dict() for role in roles]), 200

@role_bp.route('/roles', methods=['POST'])
@login_required
@requires_role('admin')
def create_role():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    parent_id = data.get('parent_id')
    role, error = create_role_service(name, description, parent_id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Role created", "id": role.id}), 201

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
@login_required
@requires_role('admin')
def update_role(role_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    role, error = update_role_service(role_id, name, description)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Role updated", "id": role.id}), 200

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@login_required
@requires_role('admin')
def delete_role(role_id):
    success, error = delete_role_service(role_id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Role deleted"}), 200
