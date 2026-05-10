from src.database import Database
import flet as ft
from datetime import datetime


class CtrlTransacao:
    def __init__(self):
        self.db = Database()

    def converter_data(self, data):
        formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]

        for fmt in formatos:
            try:
                return datetime.strptime(data, fmt)
            except:
                continue

        return None

    def buscar_transacoes(self):
        conn = self.db.conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                t.id,
                t.tipo,
                t.valor,
                t.descricao,
                t.data,
                t.categoria,
                t.observacao,
                c.txt_icon,
                c.color_icon
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria = c.nome AND t.tipo = c.tipo
            ORDER BY t.data DESC
        """)

        dados = cursor.fetchall()
        conn.close()

        lista = []

        for  id_, tipo, valor, descricao, data, categoria, observacao, icon_str, cor_icon in dados:

            dt = self.converter_data(data)

            # valor
            if tipo == "despesa":
                valor_txt = f"- R$ {abs(valor):.2f}"
                cor = "red"
            else:
                valor_txt = f"+ R$ {abs(valor):.2f}"
                cor = "green"

            # ícone
            try:
                icone = getattr(ft.CupertinoIcons, icon_str)
            except:
                icone = getattr(ft.Icons, (icon_str or "").upper(), ft.Icons.CATEGORY)

            cor_icon = cor_icon or "#6B7280"

            # data formatada para UI
            if dt:
                data_formatada = dt.strftime("%d %b")
            else:
                data_formatada = data or ""

            lista.append({
                "id": id_,
                "descricao": descricao or "Sem descrição",
                "observacao" : observacao,
                "categoria": categoria or "",
                "data": data_formatada,   
                "data_raw": dt, 
                "valor": valor_txt,
                "cor": cor,
                "icone": icone,
                "cor_icon": cor_icon,
                "tipo": tipo,
            })

        return lista

    def deletar(self, id_):
        conn = self.db.conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id=?", (id_,))
        conn.commit()
        conn.close()