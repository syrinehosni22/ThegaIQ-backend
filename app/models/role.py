from app import db
from app.models.associations import role_capabilities
from app.models.capability import Capability  # make sure Capability is imported

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    parent = db.relationship('Role', remote_side=[id], backref='children')
    capabilities = db.relationship('Capability', secondary=role_capabilities, back_populates='roles')

    def to_dict(self, include_descendants=False):
        """
        Convert Role to dictionary including capabilities.
        :param include_descendants: if True, include capabilities from all descendant roles.
        """
        if include_descendants:
            # get capabilities including all descendants
            caps = self.all_capabilities()
        else:
            # only direct capabilities
            caps = set(self.capabilities or [])

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parent_id": self.parent_id,
            "capabilities": [cap.name for cap in caps]
        }

    def get_all_descendants(self):
        """
        Return a set of Role objects that are descendants of this role
        (children, grandchildren, ...). Depth-first traversal.
        """
        descendants = set()
        stack = list(self.children or [])
        while stack:
            r = stack.pop()
            if r not in descendants:
                descendants.add(r)
                stack.extend(r.children or [])
        return descendants

    def all_capabilities(self):
        """
        Return a set of Capability objects assigned to this role
        AND to all descendant roles (implements parent-is-superior logic).
        """
        caps = set(self.capabilities or [])
        for desc in self.get_all_descendants():
            caps |= set(desc.capabilities or [])
        return caps
