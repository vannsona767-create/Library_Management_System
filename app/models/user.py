from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager


class User(db.Model, UserMixin):
    """A registered library user. role is either 'admin' or 'user'."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', name='user_role'),
                      nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user can have many borrowing records.
    # cascade='all, delete-orphan' matches the ON DELETE CASCADE in the SQL schema.
    borrowings = db.relationship('Borrowing', backref='user', lazy=True,
                                  cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store a plain-text password. Never store plain text."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Tells Flask-Login how to load a user from the session cookie."""
    return User.query.get(int(user_id))
