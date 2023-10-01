from flask import Blueprint, render_template


routes_bp = Blueprint('routes_bp', __name__,
    template_folder='frontend/views',
    static_folder='frontend/static',
    static_url_path='frontend/assets')


@routes_bp.route('/')
def homePage():
    return render_template('index.html')