from datetime import date, timedelta

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Book, Borrowing, User
from app.routes.admin import admin_required

borrowings_bp = Blueprint('borrowings', __name__, url_prefix='/borrowings')

# How long a user gets to keep a book
LOAN_PERIOD_DAYS = 14


def refresh_overdue_statuses():
    """Mark any still-out borrowings whose due date has passed as 'Overdue'.

    Called before showing borrowing lists so statuses stay accurate without
    needing a background job - simple and good enough for this project.
    """
    overdue = Borrowing.query.filter(
        Borrowing.status == 'Borrowed',
        Borrowing.due_date < date.today()
    ).all()

    if overdue:
        for record in overdue:
            record.status = 'Overdue'
        db.session.commit()


@borrowings_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Rule 1: must have a copy on the shelf
    if book.available_quantity <= 0:
        flash('Sorry, all copies of that book are currently out.', 'error')
        return redirect(url_for('books.book_detail', book_id=book.id))

    # Rule 2: no double-borrowing the same title
    existing = Borrowing.query.filter(
        Borrowing.user_id == current_user.id,
        Borrowing.book_id == book.id,
        Borrowing.status.in_(['Borrowed', 'Overdue'])
    ).first()

    if existing:
        flash('You already have a copy of that book out.', 'error')
        return redirect(url_for('books.book_detail', book_id=book.id))

    today = date.today()
    borrowing = Borrowing(
        user_id=current_user.id,
        book_id=book.id,
        borrow_date=today,
        due_date=today + timedelta(days=LOAN_PERIOD_DAYS),
        status='Borrowed',
    )

    # Take a copy off the shelf
    book.available_quantity -= 1

    db.session.add(borrowing)
    db.session.commit()

    flash(
        f'You borrowed "{book.title}". Please return it by {borrowing.due_date.strftime("%d %b %Y")}.',
        'success'
    )
    return redirect(url_for('borrowings.my_borrowings'))


@borrowings_bp.route('/return/<int:borrowing_id>', methods=['POST'])
@login_required
def return_book(borrowing_id):
    borrowing = Borrowing.query.get_or_404(borrowing_id)

    # Users may only return their own loans; admins may return any
    if borrowing.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    if borrowing.status == 'Returned':
        flash('That book has already been returned.', 'error')
        return redirect(url_for('borrowings.my_borrowings'))

    borrowing.return_date = date.today()
    borrowing.status = 'Returned'

    # Put the copy back on the shelf, without exceeding the total owned
    book = borrowing.book
    if book.available_quantity < book.quantity:
        book.available_quantity += 1

    db.session.commit()

    flash(f'You returned "{book.title}". Thank you!', 'success')

    if current_user.is_admin and request.form.get('from') == 'admin':
        return redirect(url_for('borrowings.all_borrowings'))
    return redirect(url_for('borrowings.my_borrowings'))


@borrowings_bp.route('/my')
@login_required
def my_borrowings():
    """The current user's active loans and past history."""
    refresh_overdue_statuses()

    active = Borrowing.query.filter(
        Borrowing.user_id == current_user.id,
        Borrowing.status.in_(['Borrowed', 'Overdue'])
    ).order_by(Borrowing.due_date).all()

    history = Borrowing.query.filter_by(
        user_id=current_user.id, status='Returned'
    ).order_by(Borrowing.return_date.desc()).all()

    return render_template(
        'user/borrowings.html',
        active=active,
        history=history,
        today=date.today(),
    )


@borrowings_bp.route('/all')
@admin_required
def all_borrowings():
    """Admin view of every borrowing record, filterable by status."""
    refresh_overdue_statuses()

    status = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Borrowing.query
    if status in ('Borrowed', 'Returned', 'Overdue'):
        query = query.filter_by(status=status)

    pagination = query.order_by(Borrowing.borrow_date.desc()).paginate(
        page=page, per_page=15, error_out=False
    )

    return render_template(
        'admin/borrowings.html',
        borrowings=pagination.items,
        pagination=pagination,
        status=status,
        today=date.today(),
    )
