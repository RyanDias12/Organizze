from src.database import Database


class Ctrl_Auth:

    def __init__(self):

        self.db = Database()

    # ==========================================
    # CADASTRO
    # ==========================================
    def cadastrar(
        self,
        nome_usuario,
        nome,
        sobrenome,
        email,
        senha,
        nascimento,
        cor_tema
    ):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO perfil
                (
                    nome_usuario,
                    nome,
                    sobrenome,
                    email,
                    senha,
                    nascimento,
                    cor_tema
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nome_usuario,
                    nome,
                    sobrenome,
                    email,
                    senha,
                    nascimento,
                    cor_tema
                )
            )

            conn.commit()

            return True, None

        except Exception as e:

            return False, str(e)

        finally:

            conn.close()

    # ==========================================
    # LOGIN
    # ==========================================
    def fazer_login(self, usuario, senha):

        conn = self.db.conectar_db()

        conn.row_factory = lambda cursor, row: {
            col[0]: row[idx]
            for idx, col in enumerate(cursor.description)
        }

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM perfil
            WHERE nome_usuario = ?
            AND senha = ?
            """,
            (usuario, senha)
        )

        perfil = cursor.fetchone()

        conn.close()

        return perfil

    # ==========================================
    # RECUPERAR SENHA
    # ==========================================
    def recuperar_senha(self, email):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT senha
            FROM perfil
            WHERE email = ?
            """,
            (email,)
        )

        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            return resultado[0]

        return None

    # ==========================================
    # VERIFICA PRIMEIRO ACESSO
    # ==========================================
    def primeiro_acesso(self):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM perfil")

        total = cursor.fetchone()[0]

        conn.close()

        return total == 0