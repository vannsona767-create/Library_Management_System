from flask import Flask

from app.config import Config
from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Connect extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import models so SQLAlchemy registers all tables
    with app.app_context():
        from app import models

    # Register routes
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.user import user

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user)

    return app