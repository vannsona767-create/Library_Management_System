from flask import Flask

from app.config import Config
from app.extensions import db, login_manager


def create_app():
    """Application factory: builds and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Connect extensions to this app instance
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # used later, once auth exists

    # Import models so SQLAlchemy registers all tables/relationships
    with app.app_context():
        from app import models  # noqa: F401

    # Register blueprints (routes). More get added in later stages.
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
