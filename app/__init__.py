from flask import Flask
from app.extensions import db, login_manager, migrate
from app.routes.auth_routes import auth_bp
from app.routes.role_routes import role_bp
from app.routes.user_routes import user_bp
from app.routes.capability_routes import capability_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

     # 👇 Add the user loader here
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
     # Import CLI commands
    from .cli import register_commands
    register_commands(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(role_bp, url_prefix="/api/role")
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(capability_bp, url_prefix='/api/capabilities')

    
    return app
