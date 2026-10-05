from .auth_controller import auth_bp
from .main_controller import main_bp

def init_app(app):
    """Função para registrar todos os controladores no app Flask."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

__all__ = ['auth_bp', 'main_bp', 'init_app']