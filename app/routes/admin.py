from functools import wraps

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db
from app.models import User, Book, Category, Borrowing

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Only allow admins through; everyone else gets a 403.
    Later stages (books, categories, users, borrowings management)
    will reuse this same decorator on every admin route.
    """
    @wraps(f)
    @login_required
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_view


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_books = Book.query.count()

    available_books = db.session.query(
        func.coalesce(func.sum(Book.available_quantity), 0)
    ).scalar()

    borrowed_books = db.session.query(
        func.coalesce(func.sum(Book.quantity - Book.available_quantity), 0)
    ).scalar()

    total_members = User.query.filter_by(role='user').count()
    total_categories = Category.query.count()
    active_borrowings = Borrowing.query.filter_by(status='Borrowed').count()
    returned_books = Borrowing.query.filter_by(status='Returned').count()

    stats = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'total_members': total_members,
        'total_categories': total_categories,
        'active_borrowings': active_borrowings,
        'returned_books': returned_books,
    }

    return render_template('admin/dashboard.html', stats=stats)
