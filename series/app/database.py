import os
import sqlite3

# Pega o caminho absoluto da pasta raiz do projeto (subindo 1 nível da pasta 'app')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'meu_sistema.db') # Altera para o nome real do teu ficheiro .db

class DatabaseConnection:
    def __enter__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row  # Permite aceder às colunas pelo nome
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()