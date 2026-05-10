from src.database import Database
import flet as ft

class Ctrl_Nova_transacao:
    def __init__(self):
        self.db = Database()

    def buscar_categorias(self, tipo):
        conn = self.db.conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nome, txt_icon, color_icon
            FROM categorias
            WHERE tipo=?
        """, (tipo,))

        dados = cursor.fetchall()
        conn.close()

        categorias_formatadas = []

        for nome, icon_str, cor in dados:
            try:
                icone = getattr(ft.CupertinoIcons, icon_str)
            except:
                icone = getattr(ft.Icons, icon_str, ft.Icons.CATEGORY)

            bg = "#F3F4F6"
            categorias_formatadas.append((nome, icone, cor, bg))

        return categorias_formatadas

    def salvar_transacao(self, tipo, valor, descricao, data, categoria, obs):
        """
        Retorna (sucesso: bool, mensagem_erro: str | None)
        """
        try:
            conn = self.db.conectar_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO transacoes 
                (tipo, valor, descricao, data, categoria, observacao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tipo, valor, descricao, data, categoria, obs))
            
            conn.commit()
            conn.close()
            
            return True, None   # Sucesso
            
        except Exception as e:
            erro_msg = str(e)
            print(f"Erro ao salvar transação: {erro_msg}")
            
            if "UNIQUE" in erro_msg or "already exists" in erro_msg:
                erro_msg = "Já existe uma transação com esses dados."
            elif "no such table" in erro_msg:
                erro_msg = "Erro no banco de dados: tabela não encontrada."
            elif "NOT NULL" in erro_msg:
                erro_msg = "Campos obrigatórios estão faltando."
                
            return False, erro_msg