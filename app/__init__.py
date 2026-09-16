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

    # Register blueprints (routes). More get added in later stages.
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
