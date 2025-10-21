from app import db

# Association table between roles and capabilities
role_capabilities = db.Table(
    'role_capabilities',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('capability_id', db.Integer, db.ForeignKey('capabilities.id'), primary_key=True)
)
