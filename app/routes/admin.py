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
    # Imported locally: borrowings.py imports admin_required from this module,
    # so a top-level import here would be circular.
    from app.routes.borrowings import refresh_overdue_statuses
    refresh_overdue_statuses()

    total_books = Book.query.count()

    available_books = db.session.query(
        func.coalesce(func.sum(Book.available_quantity), 0)
    ).scalar()

    borrowed_books = db.session.query(
        func.coalesce(func.sum(Book.quantity - Book.available_quantity), 0)
    ).scalar()

    total_members = User.query.filter_by(role='user').count()
    total_categories = Category.query.count()
    # Overdue loans are still active - the book is out
    active_borrowings = Borrowing.query.filter(
        Borrowing.status.in_(['Borrowed', 'Overdue'])
    ).count()
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
