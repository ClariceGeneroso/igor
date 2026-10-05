from werkzeug.security import generate_password_hash, check_password_hash
from app.database import DatabaseConnection

class UserModel:
    def __init__(self, username: str, password_hash: str = None, id: int = None):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    # --- MÉTODOS DE INSTÂNCIA ---

    def set_password(self, password: str):
        """Gera o hash da senha e atribui ao atributo de instância."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica se a senha em texto limpo corresponde ao hash guardado."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def salvar(self) -> bool:
        """Insere um novo utilizador ou atualiza um utilizador existente."""
        with DatabaseConnection() as cursor:
            if self.id is None:
                query = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
                cursor.execute(query, (self.username, self.password_hash))
                self.id = cursor.lastrowid
            else:
                query = "UPDATE users SET username = ?, password_hash = ? WHERE id = ?"
                cursor.execute(query, (self.username, self.password_hash, self.id))
            return True

    def deletar(self) -> bool:
        """Remove a própria instância da base de dados."""
        if self.id is None:
            return False
        with DatabaseConnection() as cursor:
            query = "DELETE FROM users WHERE id = ?"
            cursor.execute(query, (self.id,))
            return True

    # --- MÉTODOS DE CLASSE / BUSCAS ---

    @classmethod
    def _converter_linha_para_objeto(cls, row):
        """Método auxiliar interno para converter um registo sqlite3.Row num objeto UserModel."""
        if row is None:
            return None
        return cls(
            id=row['id'],
            username=row['username'],
            password_hash=row['password_hash']
        )

    @classmethod
    def get_by_username(cls, username: str):
        """Procura um utilizador pelo nome de utilizador e retorna uma instância de UserModel."""
        query = "SELECT id, username, password_hash FROM users WHERE username = ?"
        with DatabaseConnection() as cursor:
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            return cls._converter_linha_para_objeto(row)

    @classmethod
    def get_by_id(cls, user_id: int):
        """Procura um utilizador pelo ID e retorna uma instância de UserModel."""
        query = "SELECT id, username, password_hash FROM users WHERE id = ?"
        with DatabaseConnection() as cursor:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            return cls._converter_linha_para_objeto(row)

    @classmethod
    def get_all(cls):
        """Retorna uma lista com todos os utilizadores como objetos UserModel."""
        query = "SELECT id, username, password_hash FROM users"
        with DatabaseConnection() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [cls._converter_linha_para_objeto(row) for row in rows]