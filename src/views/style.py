import flet as ft
import sqlite3

# =========================================================
# FUNÇÃO CARREGAR TEMA
# =========================================================
def carregar_cor_tema():

    try:

        conn = sqlite3.connect("src/organizze.db")

        cursor = conn.cursor()

        cursor.execute("""
            SELECT cor_tema
            FROM perfil
            LIMIT 1
        """)

        resultado = cursor.fetchone()

        conn.close()

        if not resultado:
            return "#3AC396"

        tema = resultado[0]

        cores = {
            "Azul": "#2563EB",
            "Verde": "#3AC396",
            "Roxo": "#9333EA",
            "Vermelho": "#EF4444",
            "Laranja": "#F97316",
        }

        return cores.get(tema, "#3AC396")

    except:
        return "#3AC396"


# =========================================================
# CORES PROJETO
# =========================================================

cor_tema_principal = carregar_cor_tema()

cor_background_principal = "#F6F7F9"

cor_navegacao_icons = "#6E6E6E"

# =========================================================
# TEXTOS
# =========================================================

cor_text_padrao = ft.Colors.BLACK_87

cor_text_aux = "#5A5858"