from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db
from app.models import Book, Borrowing

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    currently_borrowed = Borrowing.query.filter_by(
        user_id=current_user.id, status='Borrowed'
    ).count()

    total_borrowed = Borrowing.query.filter_by(user_id=current_user.id).count()

    overdue = Borrowing.query.filter_by(
        user_id=current_user.id, status='Overdue'
    ).count()

    available_books = db.session.query(
        func.coalesce(func.sum(Book.available_quantity), 0)
    ).scalar()

    stats = {
        'currently_borrowed': currently_borrowed,
        'total_borrowed': total_borrowed,
        'overdue': overdue,
        'available_books': available_books,
    }

    return render_template('user/dashboard.html', stats=stats)
