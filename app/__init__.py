from flask import Flask
from app.extensions import db, login_manager, migrate
from app.routes.auth_routes import auth_bp
from app.routes.role_routes import role_bp
from app.config import Config
from app.models import User  # adjust the import path to your project structure

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

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(role_bp, url_prefix="/api/admin")


    return app
