from functools import wraps
from flask import request, session, redirect, url_for, flash


PUBLIC_ENDPOINTS = ['auth.login', 'static']

def init_auth_middleware(app):
    """
    Hook global que bloqueia o acesso a qualquer rota privada
    se o usuário não estiver autenticado na sessão.
    """
    @app.before_request
    def check_authentication():
        endpoint = request.endpoint

        if not endpoint or any(endpoint.startswith(pub) for pub in PUBLIC_ENDPOINTS):
            return None

        if 'user' not in session:
            flash("Por favor, faça login para acessar esta página.", "warning")
            return redirect(url_for('auth.login'))

def guest_only(f):
    """
    Decorator com @wraps para proibir o acesso de usuários já autenticados 
    a telas de visitantes (como a tela de Login).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('auth.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """
    Decorator individual com @wraps para rotas que exigem login explícito.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Por favor, faça login para acessar esta página.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function