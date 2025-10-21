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

    def to_dict(self):
        capabilities = set()

        for role in self.roles:
        # Add capabilities of the role itself
            for cap in role.capabilities:
                capabilities.add(cap.name)
        
        # If the role has a parent, also include its capabilities
            if role.parent:
                for cap in role.parent.capabilities:
                    capabilities.add(cap.name)

        return {
           "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "roles": [role.name for role in self.roles],
            "capabilities": list(capabilities)
        }
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
