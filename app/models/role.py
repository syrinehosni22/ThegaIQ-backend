from app import db

from app.models.capability import Capability 
role_capabilities = db.Table(
    'role_capabilities',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('capability_id', db.Integer, db.ForeignKey('capabilities.id'))
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    parent = db.relationship('Role', remote_side=[id], backref='children')
    capabilities = db.relationship('Capability', secondary=role_capabilities, back_populates='roles')

    def all_capabilities(self):
        caps = set(self.capabilities)
        if self.parent:
            caps |= set(self.parent.all_capabilities())
        return caps
