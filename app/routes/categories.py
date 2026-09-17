from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models import Category
from app.routes.admin import admin_required

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
@admin_required
def manage_categories():
    """List all categories, with optional search."""
    search = request.args.get('search', '').strip()

    query = Category.query
    if search:
        query = query.filter(Category.name.ilike(f'%{search}%'))

    categories = query.order_by(Category.name).all()

    return render_template('admin/categories.html',
                            categories=categories, search=search)


@categories_bp.route('/add', methods=['POST'])
@admin_required
def add_category():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()

    if not name:
        flash('Category name is required.', 'error')
        return redirect(url_for('categories.manage_categories'))

    if Category.query.filter_by(name=name).first():
        flash(f'A category named "{name}" already exists.', 'error')
        return redirect(url_for('categories.manage_categories'))

    category = Category(name=name, description=description or None)
    db.session.add(category)
    db.session.commit()

    flash(f'Category "{name}" was added.', 'success')
    return redirect(url_for('categories.manage_categories'))


@categories_bp.route('/<int:category_id>/edit', methods=['POST'])
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()

    if not name:
        flash('Category name is required.', 'error')
        return redirect(url_for('categories.manage_categories'))

    # Name must stay unique, ignoring this category itself
    existing = Category.query.filter_by(name=name).first()
    if existing and existing.id != category.id:
        flash(f'A category named "{name}" already exists.', 'error')
        return redirect(url_for('categories.manage_categories'))

    category.name = name
    category.description = description or None
    db.session.commit()

    flash(f'Category "{name}" was updated.', 'success')
    return redirect(url_for('categories.manage_categories'))


@categories_bp.route('/<int:category_id>/delete', methods=['POST'])
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # The schema uses ON DELETE SET NULL, so books survive but become
    # uncategorized. Warn about how many are affected rather than blocking.
    book_count = len(category.books)
    name = category.name

    db.session.delete(category)
    db.session.commit()

    if book_count:
        flash(
            f'Category "{name}" was deleted. {book_count} book(s) are now uncategorized.',
            'success'
        )
    else:
        flash(f'Category "{name}" was deleted.', 'success')

    return redirect(url_for('categories.manage_categories'))
