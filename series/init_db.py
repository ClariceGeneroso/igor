import os
import sqlite3
from werkzeug.security import generate_password_hash

# Pega o caminho absoluto da raiz onde este ficheiro se encontra
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'meu_sistema.db')  # Altera para o nome do teu ficheiro .db se for diferente

def inicializar_banco():
    print(f"A conectar à base de dados em: {DB_PATH}")
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    # 1. Criar a tabela 'users'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # 2. Inserir utilizadores de teste se a tabela estiver vazia
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        usuarios_iniciais = [
            ('admin', generate_password_hash('admin123')),
            ('estudante', generate_password_hash('123456'))
        ]

        cursor.executemany(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            usuarios_iniciais
        )
        print("Utilizadores de teste criados com sucesso:")
        print(" - Usuário: admin | Senha: admin123")
        print(" - Usuário: estudante | Senha: 123456")
    else:
        print("A tabela 'users' já possui registos. Nenhum utilizador inserido.")

    conexao.commit()
    conexao.close()
    print("Inicialização da base de dados concluída!")

if __name__ == '__main__':
    inicializar_banco()