from app import db

class Capability(db.Model):
    __tablename__ = 'capabilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    roles = db.relationship('Role', secondary='role_capabilities', back_populates='capabilities')

    def to_dict(self):
        """Return a dictionary representation of the capability."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # Optionally include roles info if needed
            "roles": [role.name for role in self.roles] if self.roles else []
        }