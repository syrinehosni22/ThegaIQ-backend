from app import db
from app.models.role import Role
from app.models.capability import Capability

def get_all_roles_service():
    """Return all roles."""
    return Role.query.all()


def create_role_service(name, description=None, parent_id=None, capability_ids=None):
    """
    Create a new role.
    :param name: Role name (required)
    :param description: Role description
    :param parent_id: Optional parent role id
    :param capability_ids: Optional list of capability IDs to assign
    :return: (Role object, error message)
    """
    if Role.query.filter_by(name=name).first():
        return None, "Role already exists"

    new_role = Role(name=name, description=description, parent_id=parent_id)

    # Assign capabilities if provided
    if capability_ids:
        capabilities = Capability.query.filter(Capability.id.in_(capability_ids)).all()
        new_role.capabilities = capabilities

    db.session.add(new_role)
    db.session.commit()
    return new_role, None


def update_role_service(role_id, name=None, description=None, parent_id=None, capability_ids=None):
    """
    Update a role's details.
    :param role_id: Role ID to update
    :param name: New name
    :param description: New description
    :param parent_id: New parent role ID
    :param capability_ids: List of capability IDs to assign
    :return: (Role object, error message)
    """
    role = Role.query.get(role_id)
    if not role:
        return None, "Role not found"

    if name:
        role.name = name
    if description:
        role.description = description
    if parent_id is not None:
        role.parent_id = parent_id

    # Update capabilities if provided
    if capability_ids is not None:
        capabilities = Capability.query.filter(Capability.id.in_(capability_ids)).all()
        role.capabilities.extend(capabilities)

    db.session.commit()
    return role, None


def delete_role_service(role_id):
    """
    Delete a role by ID.
    :param role_id: Role ID
    :return: (success: bool, error message)
    """
    role = Role.query.get(role_id)
    if not role:
        return False, "Role not found"

    db.session.delete(role)
    db.session.commit()
    return True, None
