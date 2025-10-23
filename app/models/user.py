from app import db
from flask_login import UserMixin
from datetime import datetime
from app.models.role import Role


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)  # access control
    roles = db.relationship('Role', secondary=user_roles)

    def all_roles(self):
        """
        Return all roles directly assigned to the user plus
        all descendant roles (roles of roles’ children).
        """
        roles = set(self.roles)
        for role in self.roles:
            roles |= role.get_all_descendants()
        return roles

    def all_capabilities(self):
        """
        Return all capabilities from all the user's roles,
        including capabilities inherited from child roles.
        """
        capabilities = set()
        for role in self.all_roles():
            capabilities |= set(role.all_capabilities())
        return {cap.name for cap in capabilities}

    def to_dict(self):
        """Serialize user data with full role and capability hierarchy."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "roles": [role.name for role in self.roles],
            "capabilities": list(self.all_capabilities()),
        }
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
