import os
from flask import Flask
from app.controllers import init_app as init_controllers
from app.middlewares import init_auth_middleware

def create_app():
    app = Flask(__name__, template_folder='views')
    app.secret_key = os.getenv('SECRET_KEY', 'chave_secreta_dev_mude_em_producao')

    # 1. Inicializa os middlewares de autenticação
    init_auth_middleware(app)

    # 2. Inicializa e registra os controllers/blueprints
    init_controllers(app)

    return app