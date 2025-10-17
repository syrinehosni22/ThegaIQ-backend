from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import auth_routes, role_routes, capability_routes
    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(role_routes.role_bp)
    app.register_blueprint(capability_routes.capability_bp)

    return app
