from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():

    return "Library Management System - Stage 1 setup OK"
