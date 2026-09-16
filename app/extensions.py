from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# These are created here (without an app) and "attached" to the app
# inside create_app(). This avoids circular imports between files.
db = SQLAlchemy()
login_manager = LoginManager()
