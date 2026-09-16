from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    # Temporary response just to confirm the app boots.
    # This will be replaced with render_template('home.html') later.
    return "Library Management System - Stage 1 setup OK"
