from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.services.role_service import (
    create_role_service,
    get_all_roles_service,
    update_role_service,
    delete_role_service
)
from app.decorators.auth_decorators import requires_role
from app.decorators.capability_role import requires_capability

role_bp = Blueprint('role_bp', __name__, template_folder='templates/roles')


def wants_json_response():
    """Helper: detect if the request wants JSON (API)."""
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html'] \
        or request.args.get('format') == 'json'


# ✅ Get All Roles
@role_bp.route('/all', methods=['GET'])
@login_required
@requires_role('Administrator')
@requires_capability(('view_all_roles'))
def get_roles():
    roles = get_all_roles_service()

    if wants_json_response():
        return jsonify([role.to_dict() for role in roles]), 200

    return render_template('list.html', roles=roles)


# ✅ Create Role
@role_bp.route('/new', methods=['GET', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_add_roles'))
def create_role():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        name = data.get('name')
        description = data.get('description')
        parent_id = data.get('parent_id')

        role, error = create_role_service(name, description, parent_id)
        if error:
            if wants_json_response():
                return jsonify({"error": error}), 400
            flash(error, 'danger')
            return redirect(url_for('role_bp.get_roles'))

        if wants_json_response():
            return jsonify(role.to_dict()), 201

        flash("Role created successfully!", "success")
        return redirect(url_for('role_bp.get_roles'))

    return render_template('create.html')


# ✅ Update Role
@role_bp.route('/<int:role_id>/edit', methods=['GET', 'PUT', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_modify_roles'))
def update_role(role_id):
    if request.method in ['PUT', 'POST']:
        data = request.get_json() if request.is_json else request.form
        name = data.get('name')
        description = data.get('description')
        parent_id = data.get('parent_id')
        capability_ids = data.getlist('capabilities') if not request.is_json else data.get('capabilities')

        role, error = update_role_service(role_id, name, description, parent_id, capability_ids)
        if error:
            if wants_json_response():
                return jsonify({"error": error}), 400
            flash(error, 'danger')
            return redirect(url_for('role_bp.get_roles'))

        if wants_json_response():
            return jsonify(role.to_dict()), 200

        flash("Role updated successfully!", "success")
        return redirect(url_for('role_bp.get_roles'))

    # GET: render form for editing
    roles = get_all_roles_service()
    current_role = next((r for r in roles if r.id == role_id), None)
    if not current_role:
        flash("Role not found", "danger")
        return redirect(url_for('role_bp.get_roles'))
    return render_template('edit.html', role=current_role, roles=roles)


# ✅ Delete Role
@role_bp.route('/<int:role_id>/delete', methods=['DELETE', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_delete_roles'))
def delete_role(role_id):
    success, error = delete_role_service(role_id)
    if error:
        if wants_json_response():
            return jsonify({"error": error}), 400
        flash(error, 'danger')
        return redirect(url_for('role_bp.get_roles'))

    if wants_json_response():
        return jsonify({"message": "Role deleted"}), 200

    flash("Role deleted successfully!", "success")
    return redirect(url_for('role_bp.get_roles'))
