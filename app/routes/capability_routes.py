from flask import Blueprint, jsonify, request
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

capability_bp = Blueprint('capability_bp', __name__)

# ✅ Get All Capabilities
@capability_bp.route('/all', methods=['GET'])
@login_required
@requires_role('Administrator')
@requires_capability(('view_all_capabilities'))
def get_capabilities():
    capabilities = get_all_capabilities_service()
    return jsonify([c.to_dict() for c in capabilities]), 200

# ✅ Get One Capability
@capability_bp.route('/<int:capability_id>', methods=['GET'])
@login_required
@requires_role('Administrator')
def get_capability(capability_id):
    capability = get_capability_by_id_service(capability_id)
    if not capability:
        return jsonify({"error": "Capability not found"}), 404
    return jsonify(capability.to_dict()), 200

# ✅ Create Capability
@capability_bp.route('/new', methods=['POST'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_add_capabilities'))
def create_capability():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    capability, error = create_capability_service(name, description)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({
        "message": "Capability created successfully",
        "capability": capability.to_dict()
    }), 201

# ✅ Update Capability
@capability_bp.route('/<int:capability_id>', methods=['PUT'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_modify_capabilities'))
def update_capability(capability_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    capability, error = update_capability_service(capability_id, name, description)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({
        "message": "Capability updated successfully",
        "capability": capability.to_dict()
    }), 200

# ✅ Delete Capability
@capability_bp.route('/<int:capability_id>', methods=['DELETE'])
@login_required
@requires_role('Administrator')
@requires_capability(('can_delete_capabilities'))
def delete_capability(capability_id):
    success, error = delete_capability_service(capability_id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Capability deleted successfully"}), 200
