from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.user import user
    app.register_blueprint(user)

    return app