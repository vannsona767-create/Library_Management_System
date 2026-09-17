from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from app.extensions import db
from app.models import Book, Borrowing, User
from app.routes.borrowings import refresh_overdue_statuses

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    # Keep 'Overdue' accurate before counting
    refresh_overdue_statuses()

    currently_borrowed = Borrowing.query.filter(
        Borrowing.user_id == current_user.id,
        Borrowing.status.in_(['Borrowed', 'Overdue'])
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


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit your own profile, including changing your password."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        errors = []

        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email is required.')

        if username and User.query.filter(
                User.username == username, User.id != current_user.id).first():
            errors.append('That username is already taken.')
        if email and User.query.filter(
                User.email == email, User.id != current_user.id).first():
            errors.append('That email is already registered.')

        # Password change is optional - only validate if they filled it in
        changing_password = bool(new_password or confirm_password)
        if changing_password:
            if not current_password:
                errors.append('Enter your current password to set a new one.')
            elif not current_user.check_password(current_password):
                errors.append('Your current password is incorrect.')

            if len(new_password) < 6:
                errors.append('New password must be at least 6 characters.')
            if new_password != confirm_password:
                errors.append('New passwords do not match.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('user.profile'))

        current_user.username = username
        current_user.email = email
        if changing_password:
            current_user.set_password(new_password)

        db.session.commit()

        flash('Your profile was updated.', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/profile.html')
