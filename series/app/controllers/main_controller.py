from flask import Blueprint, render_template, session
from app.middlewares import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """Página principal / Home do sistema."""
    return render_template('dashboard.html', username=session.get('user'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Apenas um alias para a home."""
    return render_template('dashboard.html', username=session.get('user'))