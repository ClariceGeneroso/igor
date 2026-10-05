import os
from app import create_app

# Instancia a aplicação Flask através da factory
app = create_app()

if __name__ == '__main__':
    # Habilita o modo de depuração para recarregar o servidor automaticamente ao alterar arquivos
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1']
    
    # Roda a aplicação na porta 5000
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)

import os

# Caminho apontando para o arquivo database.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'database.db')