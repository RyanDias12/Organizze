from src.database import Database


class Ctrl_Metas:
    def __init__(self):
        self.db = Database()

    # =========================
    # CRIAR META
    # =========================
    def criar_meta(self, valor_atual, valor_meta, descricao, data_criacao, data_limite):

        conn = None

        try:
            conn = self.db.conectar_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO metas
                (valor_atual, valor_meta, descricao, data_criacao, data_limite)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    valor_atual,
                    valor_meta,
                    descricao,
                    data_criacao,
                    data_limite
                )
            )

            conn.commit()

            return True, None

        except Exception as e:

            erro_msg = str(e)
            print(f"Erro ao salvar Meta: {erro_msg}")

            if "UNIQUE" in erro_msg:
                erro_msg = "Já existe uma meta com esses dados."

            elif "no such table" in erro_msg:
                erro_msg = "Tabela metas não encontrada."

            elif "NOT NULL" in erro_msg:
                erro_msg = "Campos obrigatórios faltando."

            return False, erro_msg

        finally:
            if conn:
                conn.close()

    # =========================
    # LISTAR METAS
    # =========================
    def listar_meta(self):

        conn = None

        try:
            conn = self.db.conectar_db()

            # retorna dicionário
            conn.row_factory = lambda cursor, row: {
                col[0]: row[idx]
                for idx, col in enumerate(cursor.description)
            }

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM metas
                ORDER BY id DESC
            """)

            metas = cursor.fetchall()

            return metas

        except Exception as e:

            print(f"Erro ao listar metas: {e}")

            return []

        finally:
            if conn:
                conn.close()

    # =========================
    # ATUALIZAR META
    # =========================
    def update_meta(
        self,
        id_meta,
        valor_atual,
        valor_meta,
        descricao,
        data_limite
    ):

        conn = None

        try:
            conn = self.db.conectar_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE metas
                SET
                    valor_atual = ?,
                    valor_meta = ?,
                    descricao = ?,
                    data_limite = ?
                WHERE id = ?
                """,
                (
                    valor_atual,
                    valor_meta,
                    descricao,
                    data_limite,
                    id_meta
                )
            )

            conn.commit()

            return True, None

        except Exception as e:

            erro_msg = str(e)

            print(f"Erro ao atualizar meta: {erro_msg}")

            return False, erro_msg

        finally:
            if conn:
                conn.close()

    # =========================
    # DELETAR META
    # =========================
    def delete_meta(self, id_meta):

        conn = None

        try:
            conn = self.db.conectar_db()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM metas
                WHERE id = ?
                """,
                (id_meta,)
            )

            conn.commit()

            return True, None

        except Exception as e:

            erro_msg = str(e)

            print(f"Erro ao deletar meta: {erro_msg}")

            return False, erro_msg

        finally:
            if conn:
                conn.close()