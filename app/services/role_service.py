from app import db
from app.models.role import Role

def get_all_roles_service():
    return Role.query.all()

def create_role_service(name, description=None, parent_id=None):
    if Role.query.filter_by(name=name).first():
        return None, "Role already exists"
    new_role = Role(name=name, description=description, parent_id=parent_id)
    db.session.add(new_role)
    db.session.commit()
    return new_role, None

def update_role_service(role_id, name=None, description=None):
    role = Role.query.get(role_id)
    if not role:
        return None, "Role not found"
    if name:
        role.name = name
    if description:
        role.description = description
    db.session.commit()
    return role, None

def delete_role_service(role_id):
    role = Role.query.get(role_id)
    if not role:
        return False, "Role not found"
    db.session.delete(role)
    db.session.commit()
    return True, None
