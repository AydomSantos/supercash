from passlib.hash import pbkdf2_sha256
from config.database import Database

class Usuario:
    def __init__(self, id=None, username=None, password=None, nome=None, nivel_acesso=None):
        self.id = id
        self.username = username
        self.password_hash = None if password is None else self.hash_password(password)
        self.nome = nome
        # Store nivel_acesso as string to maintain consistency
        self.nivel_acesso = str(nivel_acesso).lower() if nivel_acesso else 'user'
        self.db = Database()

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    def save(self):
        conn = None
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            if self.id is None:
                # Insert new user
                cur.execute("""
                    INSERT INTO usuarios (username, password_hash, nome, nivel_acesso)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (self.username, self.password_hash, self.nome, self.nivel_acesso))
                self.id = cur.fetchone()[0]
            else:
                # Update existing user
                cur.execute("""
                    UPDATE usuarios
                    SET username = %s, password_hash = %s, nome = %s, nivel_acesso = %s
                    WHERE id = %s
                """, (self.username, self.password_hash, self.nome, self.nivel_acesso, self.id))
            
            cur.close()
            return self.id
        finally:
            if conn:
                self.db.return_connection(conn)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.get_by_username(username)
        if user and user.verify_password(password):
            return user
        return None

    @classmethod
    def get_by_username(cls, username):
        db = Database()
        conn = None
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            user_data = cur.fetchone()
            
            cur.close()
            
            if user_data:
                user = cls(
                    id=user_data[0],
                    username=user_data[1],
                    nome=user_data[3],
                    nivel_acesso=user_data[4]
                )
                user.password_hash = user_data[2]  # Load password hash for verification
                return user
            return None
        finally:
            if conn:
                db.return_connection(conn)

    @classmethod
    def get_by_id(cls, user_id):
        db = Database()
        conn = None
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            
            cur.close()
            
            if user_data:
                return cls(
                    id=user_data[0],
                    username=user_data[1],
                    password=None,
                    nome=user_data[3],
                    nivel_acesso=user_data[4]
                )
            return None
        finally:
            if conn:
                db.return_connection(conn)

    @classmethod
    def get_all(cls):
        db = Database()
        conn = None
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM usuarios ORDER BY nome")
            users = []
            
            for user_data in cur.fetchall():
                users.append(cls(
                    id=user_data[0],
                    username=user_data[1],
                    password=None,
                    nome=user_data[3],
                    nivel_acesso=user_data[4]
                ))
            
            cur.close()
            return users
        finally:
            if conn:
                db.return_connection(conn)

    def delete(self):
        if self.id is None:
            return False
            
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (self.id,))
            success = cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            success = False
        finally:
            cur.close()
            
        return success