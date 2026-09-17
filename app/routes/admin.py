from functools import wraps

from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
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


# =====================================================================
# Member / user management
# =====================================================================

@admin_bp.route('/users')
@admin_required
def manage_users():
    """List all users, with optional search by username or email."""
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)

    query = User.query
    if search:
        like = f'%{search}%'
        query = query.filter(
            db.or_(User.username.ilike(like), User.email.ilike(like))
        )

    pagination = query.order_by(User.username).paginate(
        page=page, per_page=15, error_out=False
    )

    return render_template('admin/users.html',
                            users=pagination.items,
                            pagination=pagination,
                            search=search)


@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """Show one member's details and their full borrowing history."""
    from app.routes.borrowings import refresh_overdue_statuses
    refresh_overdue_statuses()

    user = User.query.get_or_404(user_id)

    borrowings = Borrowing.query.filter_by(user_id=user.id) \
        .order_by(Borrowing.borrow_date.desc()).all()

    active_count = sum(1 for b in borrowings if b.status in ('Borrowed', 'Overdue'))

    return render_template('admin/user_detail.html',
                            member=user,
                            borrowings=borrowings,
                            active_count=active_count)


@admin_bp.route('/users/<int:user_id>/edit', methods=['POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    role = request.form.get('role', '').strip()

    errors = []
    if not username:
        errors.append('Username is required.')
    if not email:
        errors.append('Email is required.')
    if role not in ('admin', 'user'):
        errors.append('Role must be either admin or user.')

    # Don't let an admin strip their own admin rights and lock themselves out
    if user.id == current_user.id and role != 'admin':
        errors.append('You cannot remove your own admin role.')

    if username and User.query.filter(User.username == username, User.id != user.id).first():
        errors.append('That username is already taken.')
    if email and User.query.filter(User.email == email, User.id != user.id).first():
        errors.append('That email is already registered.')

    if errors:
        for e in errors:
            flash(e, 'error')
        return redirect(url_for('admin.user_detail', user_id=user.id))

    user.username = username
    user.email = email
    user.role = role
    db.session.commit()

    flash(f'{user.username} was updated.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Guard: never delete yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.manage_users'))

    # Guard: don't delete anyone still holding books
    active = Borrowing.query.filter(
        Borrowing.user_id == user.id,
        Borrowing.status.in_(['Borrowed', 'Overdue'])
    ).count()

    if active:
        flash(
            f'{user.username} still has {active} book(s) out. '
            'Those must be returned before the account can be deleted.',
            'error'
        )
        return redirect(url_for('admin.manage_users'))

    username = user.username
    db.session.delete(user)
    db.session.commit()

    flash(f'{username} was deleted.', 'success')
    return redirect(url_for('admin.manage_users'))
