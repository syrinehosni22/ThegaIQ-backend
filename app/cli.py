import click
from flask.cli import with_appcontext
from . import db
from .models import User, Role
from werkzeug.security import generate_password_hash


def register_commands(app):
    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("email")
    @click.argument("password")
    @with_appcontext
    def create_admin(username, email, password):
        """Create a superuser/admin and assign the admin role."""
        
        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            click.echo(f"⚠️ User '{username}' already exists!")
            return

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        admin_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(admin_user)
        db.session.flush()  # so admin_user.id is available before commit

        # Check if admin role exists
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            click.echo("🆕 Creating 'admin' role...")
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.flush()

        # Link role to user (assuming many-to-many relationship)
        if hasattr(admin_user, "roles"):
            admin_user.roles.append(admin_role)
        else:
            click.echo("⚠️ The User model has no 'roles' relationship defined!")

        db.session.commit()
        click.echo(f"✅ Admin user '{username}' created successfully with 'admin' role!")
