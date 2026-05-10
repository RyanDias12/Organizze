from src.database import Database
import flet as ft
from datetime import datetime


class Ctrl_inicio:
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
                c.txt_icon,
                c.color_icon
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria = c.nome
            ORDER BY t.data DESC
            LIMIT 5
        """)

        dados = cursor.fetchall()
        conn.close()

        lista = []

        for id_, tipo, valor, descricao, data, categoria, icon_str, cor_icon in dados:

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
                "categoria": categoria or "",
                "data": data_formatada,   
                "data_raw": dt, 
                "valor": valor_txt,
                "cor": cor,
                "icone": icone,
                "cor_icon": cor_icon,
                "tipo": tipo
            })

        return lista

    def deletar(self, id_):
        conn = self.db.conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id=?", (id_,))
        conn.commit()
        conn.close()
        
        
    def buscar_gastos_por_categoria(self):
      conn = self.db.conectar_db()
      cursor = conn.cursor()

      cursor.execute("""
          SELECT 
              t.categoria,
              t.valor,
              t.data,
              c.color_icon
          FROM transacoes t
          LEFT JOIN categorias c ON t.categoria = c.nome
          WHERE t.tipo = 'despesa'
      """)

      dados = cursor.fetchall()
      conn.close()

      from datetime import datetime

      mes_atual = datetime.now().month
      ano_atual = datetime.now().year

      categorias = {}

      for categoria, valor, data, cor in dados:

          dt = self.converter_data(data)

          if not dt:
              continue

          if dt.month != mes_atual or dt.year != ano_atual:
              continue

          categoria = categoria or "Outros"
          valor = abs(valor)

          if categoria not in categorias:
              categorias[categoria] = {
                  "total": 0,
                  "cor": cor or "#6B7280"
              }

          categorias[categoria]["total"] += valor

      if not categorias:
          return []

      total_geral = sum(c["total"] for c in categorias.values())

      resultado = []

      for cat, info in categorias.items():
          porcentagem = int((info["total"] / total_geral) * 100)

          resultado.append({
              "categoria": cat,
              "porcentagem": porcentagem,
              "cor": info["cor"]
          })

      # ordena maior → menor
      resultado.sort(key=lambda x: x["porcentagem"], reverse=True)
      return resultado
    
    def resumo_financeiro(self):
      conn = self.db.conectar_db()
      cursor = conn.cursor()

      cursor.execute("""
          SELECT tipo, valor, data
          FROM transacoes
      """)

      dados = cursor.fetchall()
      conn.close()

      from datetime import datetime

      mes_atual = datetime.now().month
      ano_atual = datetime.now().year

      total = 0
      receitas = 0
      despesas = 0

      for tipo, valor, data in dados:
          dt = self.converter_data(data)

          if not dt:
              continue

          # 🔥 saldo total (tudo)
          if tipo == "receita":
              total += valor
          else:
              total -= abs(valor)

          # 🔥 filtro mês atual
          if dt.month == mes_atual and dt.year == ano_atual:
              if tipo == "receita":
                  receitas += valor
              else:
                  despesas += abs(valor)

      return {
          "saldo": total,
          "receitas": receitas,
          "despesas": despesas
      }