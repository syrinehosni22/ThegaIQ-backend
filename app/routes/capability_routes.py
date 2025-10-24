from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.decorators.auth_decorators import requires_role
from app.decorators.capability_role import requires_capability
from app.services.capability_service import (
    create_capability_service,
    get_all_capabilities_service,
    get_capability_by_id_service,
    update_capability_service,
    delete_capability_service
)

capability_bp = Blueprint('capability_bp', __name__, template_folder='templates/capabilities')


def wants_json_response():
    """Helper: determine if request expects JSON."""
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html'] \
        or request.args.get('format') == 'json'


# ✅ Get All Capabilities
@capability_bp.route('/all', methods=['GET'])
@login_required
@requires_role('Administrator')
@requires_capability(('view_all_capabilities'))
def get_capabilities():
    capabilities = get_all_capabilities_service()

    if wants_json_response():
        return jsonify([c.to_dict() for c in capabilities]), 200
    return render_template('list.html', capabilities=capabilities)


# ✅ Get One Capability
@capability_bp.route('/<int:capability_id>', methods=['GET'])
@login_required
@requires_role('Administrator')
def get_capability(capability_id):
    capability = get_capability_by_id_service(capability_id)
    if not capability:
        if wants_json_response():
            return jsonify({"error": "Capability not found"}), 404
        flash("Capability not found", "danger")
        return redirect(url_for('capability_bp.get_capabilities'))

    if wants_json_response():
        return jsonify(capability.to_dict()), 200
    return render_template('detail.html', capability=capability)


# ✅ Create Capability
@capability_bp.route('/new', methods=['GET', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_add_capabilities'))
def create_capability():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        name = data.get('name')
        description = data.get('description')
        capability, error = create_capability_service(name, description)

        if error:
            if wants_json_response():
                return jsonify({"error": error}), 400
            flash(error, "danger")
            return redirect(url_for('capability_bp.get_capabilities'))

        if wants_json_response():
            return jsonify({
                "message": "Capability created successfully",
                "capability": capability.to_dict()
            }), 201

        flash("Capability created successfully!", "success")
        return redirect(url_for('capability_bp.get_capabilities'))

    # Render form if GET request (for web)
    return render_template('create.html')


# ✅ Update Capability
@capability_bp.route('/<int:capability_id>/edit', methods=['GET', 'PUT', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_modify_capabilities'))
def update_capability(capability_id):
    capability = get_capability_by_id_service(capability_id)
    if not capability:
        if wants_json_response():
            return jsonify({"error": "Capability not found"}), 404
        flash("Capability not found", "danger")
        return redirect(url_for('capability_bp.get_capabilities'))

    if request.method in ['PUT', 'POST']:
        data = request.get_json() if request.is_json else request.form
        name = data.get('name')
        description = data.get('description')
        updated_capability, error = update_capability_service(capability_id, name, description)

        if error:
            if wants_json_response():
                return jsonify({"error": error}), 400
            flash(error, "danger")
            return redirect(url_for('capability_bp.get_capabilities'))

        if wants_json_response():
            return jsonify({
                "message": "Capability updated successfully",
                "capability": updated_capability.to_dict()
            }), 200

        flash("Capability updated successfully!", "success")
        return redirect(url_for('capability_bp.get_capabilities'))

    # Render edit form if GET request
    return render_template('edit.html', capability=capability)


# ✅ Delete Capability
@capability_bp.route('/<int:capability_id>/delete', methods=['DELETE', 'POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_delete_capabilities'))
def delete_capability(capability_id):
    success, error = delete_capability_service(capability_id)
    if error:
        if wants_json_response():
            return jsonify({"error": error}), 400
        flash(error, "danger")
        return redirect(url_for('capability_bp.get_capabilities'))

    if wants_json_response():
        return jsonify({"message": "Capability deleted successfully"}), 200

    flash("Capability deleted successfully!", "success")
    return redirect(url_for('capability_bp.get_capabilities'))
