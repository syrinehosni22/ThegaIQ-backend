from app import db
from app.models.capability import Capability

# ✅ Create Capability
def create_capability_service(name, description):
    try:
        if Capability.query.filter_by(name=name).first():
            return None, "Capability already exists"
        capability = Capability(name=name, description=description)
        db.session.add(capability)
        db.session.commit()
        return capability, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

# ✅ Get All Capabilities
def get_all_capabilities_service():
    return Capability.query.all()

# ✅ Get Capability by ID
def get_capability_by_id_service(capability_id):
    return Capability.query.get(capability_id)

# ✅ Update Capability
def update_capability_service(capability_id, name, description):
    capability = Capability.query.get(capability_id)
    if not capability:
        return None, "Capability not found"
    try:
        capability.name = name or capability.name
        capability.description = description or capability.description
        db.session.commit()
        return capability, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

# ✅ Delete Capability
def delete_capability_service(capability_id):
    capability = Capability.query.get(capability_id)
    if not capability:
        return False, "Capability not found"
    try:
        db.session.delete(capability)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
