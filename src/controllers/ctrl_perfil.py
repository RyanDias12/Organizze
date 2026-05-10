from src.database import Database
from collections import defaultdict
from datetime import datetime


class Ctrl_Perfil:

    def __init__(self):

        self.db = Database()

    # =====================================================
    # SALVAR PERFIL
    # =====================================================
    def salvar_perfil(
        self,
        nome,
        sobrenome,
        nascimento,
        email,
        cor_tema
    ):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM perfil")

        existe = cursor.fetchone()[0]

        if existe == 0:

            cursor.execute("""
                INSERT INTO perfil
                (
                    nome,
                    sobrenome,
                    nascimento,
                    email,
                    cor_tema
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                nome,
                sobrenome,
                nascimento,
                email,
                cor_tema
            ))

        else:

            cursor.execute("""
                UPDATE perfil
                SET
                    nome = ?,
                    sobrenome = ?,
                    nascimento = ?,
                    email = ?,
                    cor_tema = ?
                WHERE id = 1
            """, (
                nome,
                sobrenome,
                nascimento,
                email,
                cor_tema
            ))

        conn.commit()

        conn.close()

    # =====================================================
    # CARREGAR PERFIL
    # =====================================================
    def carregar_perfil(self):

        conn = self.db.conectar_db()

        conn.row_factory = lambda cursor, row: {
            col[0]: row[idx]
            for idx, col in enumerate(cursor.description)
        }

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM perfil
            LIMIT 1
        """)

        perfil = cursor.fetchone()

        conn.close()

        return perfil

    # =====================================================
    # TOTAL TRANSACOES
    # =====================================================
    def total_transacoes(self):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM transacoes
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    # =====================================================
    # TOTAL ENTRADAS
    # =====================================================
    def total_entradas(self):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(valor)
            FROM transacoes
            WHERE tipo = 'receita'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total or 0

    # =====================================================
    # TOTAL SAIDAS
    # =====================================================
    def total_saidas(self):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(valor)
            FROM transacoes
            WHERE tipo = 'despesa'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total or 0

    # =====================================================
    # SALDO TOTAL
    # =====================================================
    def saldo_total(self):

        return self.total_entradas() - self.total_saidas()

    # =====================================================
    # METAS ATINGIDAS
    # =====================================================
    def metas_atingidas(self):

        try:

            conn = self.db.conectar_db()

            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM metas
                WHERE valor_atual >= valor_meta
            """)

            resultado = cursor.fetchone()

            conn.close()

            if resultado is None:

                return 0

            return resultado[0] or 0

        except Exception as e:

            print("Erro metas atingidas:", e)

            return 0

    # =====================================================
    # TOTAL METAS
    # =====================================================
    def total_metas(self):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM metas
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    # =====================================================
    # MÉDIA GASTOS
    # =====================================================
    def media_gastos(self):

        conn = self.db.conectar_db()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                SUM(valor),
                COUNT(DISTINCT substr(data, 1, 7))
            FROM transacoes
            WHERE tipo = 'despesa'
        """)

        resultado = cursor.fetchone()

        total_gastos = resultado[0] or 0
        total_meses = resultado[1] or 1

        conn.close()

        return total_gastos / total_meses

    # =====================================================
    # ECONOMIA TOTAL
    # =====================================================
    def economia_total(self):

        return self.saldo_total()

    # =====================================================
    # BALANÇO POR MÊS
    # =====================================================
    def balanco_mensal(self):

        conn = self.db.conectar_db()

        conn.row_factory = lambda cursor, row: {
            col[0]: row[idx]
            for idx, col in enumerate(cursor.description)
        }

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM transacoes
            ORDER BY data DESC
        """)

        transacoes = cursor.fetchall()

        conn.close()

        resultado = defaultdict(lambda: {
            "entrada": 0,
            "saida": 0,
            "saldo": 0
        })

        for t in transacoes:

            try:

                data = datetime.strptime(
                    t["data"],
                    "%d/%m/%Y"
                )

                chave = data.strftime("%B %Y").capitalize()

                if t["tipo"] == "receita":

                    resultado[chave]["entrada"] += t["valor"]

                else:

                    resultado[chave]["saida"] += t["valor"]

            except:
                pass

        for chave in resultado:

            entrada = resultado[chave]["entrada"]

            saida = resultado[chave]["saida"]

            resultado[chave]["saldo"] = entrada - saida

        return dict(resultado)