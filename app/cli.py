import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from . import db
from .models import User, Role, Capability  # Make sure Capability is imported


def register_commands(app):
    """Register custom Flask CLI commands."""

    # ========================================
    # Create admin user
    # ========================================
    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("email")
    @click.argument("password")
    @with_appcontext
    def create_admin(username, email, password):
        """Create a superuser/admin and assign the admin role."""
        if User.query.filter_by(username=username).first():
            click.echo(f"⚠️ User '{username}' already exists!")
            return

        hashed_password = generate_password_hash(password)
        admin_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(admin_user)
        db.session.flush()

        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            click.echo("🆕 Creating 'admin' role...")
            admin_role = Role(name="admin", description="Administrator role")
            db.session.add(admin_role)
            db.session.flush()

        admin_user.roles.append(admin_role)
        db.session.commit()
        click.echo(f"✅ Admin user '{username}' created successfully with 'admin' role!")

    # ========================================
    # Create role
    # ========================================
    @app.cli.command("create-role")
    @click.argument("name")
    @click.argument("description")
    @click.argument("parent-name")
    @with_appcontext
    def create_role(name, description, parent_name):
        """
        Create a new role (optionally linked to a parent role by name).
        """
        # Check if the role already exists
        if Role.query.filter_by(name=name).first():
           click.echo(f"⚠️ Role '{name}' already exists!")
           return

        parent_id = None
        if parent_name:
            parent_role = Role.query.filter_by(name=parent_name).first()
            if not parent_role:
               click.echo(f"❌ Parent role '{parent_name}' not found.")
               return
            parent_id = parent_role.id

        new_role = Role(name=name, description=description, parent_id=parent_id)
        db.session.add(new_role)
        db.session.commit()

        if parent_name:
           click.echo(f"✅ Role '{name}' created successfully with parent '{parent_name}'.")
        else:
           click.echo(f"✅ Role '{name}' created successfully without parent.")

    # ========================================
    # Create capability
    # ========================================
    @app.cli.command("create-capability")
    @click.argument("name")
    @click.argument("description")
    @with_appcontext
    def create_capability(name, description):
        """Create a new capability."""
        if Capability.query.filter_by(name=name).first():
            click.echo(f"⚠️ Capability '{name}' already exists!")
            return

        new_cap = Capability(name=name, description=description)
        db.session.add(new_cap)
        db.session.commit()
        click.echo(f"✅ Capability '{name}' created successfully!")

    # ========================================
    # Assign role to user
    # ========================================
    @app.cli.command("assign-role-user")
    @click.argument("username")
    @click.argument("role_name")
    @with_appcontext
    def assign_role_user(username, role_name):
        """Assign a role to a user."""
        user = User.query.filter_by(username=username).first()
        role = Role.query.filter_by(name=role_name).first()

        if not user:
            click.echo(f"❌ User '{username}' not found.")
            return
        if not role:
            click.echo(f"❌ Role '{role_name}' not found.")
            return

        if role in user.roles:
            click.echo(f"⚠️ User '{username}' already has role '{role_name}'.")
            return

        user.roles.append(role)
        db.session.commit()
        click.echo(f"✅ Role '{role_name}' assigned to user '{username}'.")

    # ========================================
    # Assign capability to role
    # ========================================
    @app.cli.command("assign-capabilities-role")
    @click.argument("role_name")
    @click.argument("capability_names", nargs=-1)
    @with_appcontext
    def assign_capabilities_role(role_name, capability_names):
        """
        Assign one or multiple capabilities to a role.
        """
        role = Role.query.filter_by(name=role_name).first()

        if not role:
           click.echo(f"❌ Role '{role_name}' not found.")
           return

        if not capability_names:
            click.echo("⚠️ Please provide at least one capability name.")
            return

        for name in capability_names:
            capability = Capability.query.filter_by(name=name).first()

            if not capability:
                click.echo(f"❌ Capability '{name}' not found.")
                continue

            if capability in role.capabilities:
                click.echo(f"⚠️ Role '{role_name}' already has capability '{name}'.")
                continue

            role.capabilities.append(capability)
            click.echo(f"✅ Capability '{name}' assigned to role '{role_name}'.")

        db.session.commit()
        click.echo(f"💾 All capabilities processed for role '{role_name}'.")