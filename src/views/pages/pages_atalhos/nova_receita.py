import flet as ft
from src.views.style import *
from datetime import datetime
import time
from src.controllers.ctrl_nova_transacao import Ctrl_Nova_transacao

ctrl_nova_transacao = Ctrl_Nova_transacao()




class Nova_receita_view:
    def __init__(self, on_save=None, trocar_tela = None):
        self.on_save = on_save
        self.trocar_tela = trocar_tela 

    def page(self, page: ft.Page):

        tipo = "receita"
        categoria_selecionada = {"nome": None}

        categorias_grid = ft.Row(wrap=True, spacing=10)

        def mostrar_snackbar(msg, cor="red"):
            # Criamos o snackbar
            snack = ft.SnackBar(
                content=ft.Text(msg, color="white"),
                bgcolor=cor,
                duration=2000,
                open=True  # Já nasce aberto
            )
            page.overlay.append(snack)
            page.update()

        # =========================
        # FORMATAÇÃO MOEDA
        # =========================
        def formatar_moeda(valor):
            numeros = "".join(filter(str.isdigit, valor))

            if numeros == "":
                return "R$ 0,00"

            numero = int(numeros) / 100
            return f"R$ {numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        def converter_para_float(valor):
            return float(
                valor.replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

        # =========================
        # FORMATAÇÃO DATA
        # =========================
        def formatar_data(valor):
            numeros = "".join(filter(str.isdigit, valor))[:8]

            dia = ""
            mes = ""
            ano = ""

            if len(numeros) >= 2:
                d = int(numeros[:2])
                d = max(1, min(d, 31))
                dia = f"{d:02}"
            elif len(numeros) == 1:
                dia = numeros

            if len(numeros) >= 4:
                m = int(numeros[2:4])
                m = max(1, min(m, 12))
                mes = f"{m:02}"
            elif len(numeros) == 3:
                mes = numeros[2:]

            if len(numeros) > 4:
                ano = numeros[4:8]

            if len(numeros) <= 2:
                return dia
            elif len(numeros) <= 4:
                return f"{dia}/{mes}"
            else:
                return f"{dia}/{mes}/{ano}"

        def on_change_data(e):
            e.control.value = formatar_data(e.control.value)
            e.control.update()

        # =========================
        # INPUT PADRÃO
        # =========================
        def input_padrao(label, hint=None, value=None, multiline=False):
            return ft.TextField(
                expand=True,
                label=label,
                hint_text=hint,
                value=value,
                multiline=multiline,
                min_lines=2 if multiline else 1,
                border=ft.InputBorder.OUTLINE,
                border_color="transparent",
                focused_border_color=cor_tema_principal,
                focused_border_width=2,
                filled=True,
                bgcolor="#F9FAFB",
                cursor_color=cor_tema_principal,
            )

        def on_change_valor(e):
            valor_limpo = "".join(filter(str.isdigit, e.control.value))
            valor_formatado = formatar_moeda(valor_limpo)
            e.control.value = valor_formatado
            e.control.update()

        valor_input = input_padrao("Valor (R$)", value="R$ 0,00")
        valor_input.text_align = ft.TextAlign.CENTER
        valor_input.keyboard_type = ft.KeyboardType.NUMBER
        valor_input.on_change = on_change_valor

        descricao_input = input_padrao("Descrição", hint="Ex: Supermercado")

        data_input = input_padrao(
            "Data",
            value=datetime.now().strftime("%d/%m/%Y")
        )
        data_input.keyboard_type = ft.KeyboardType.NUMBER
        data_input.on_change = on_change_data

        obs_input = input_padrao("Observações (opcional)", multiline=True)

        # =========================
        # BOTÃO CATEGORIA
        # =========================
        def btn_categoria(nome, icone, cor, bg):
            container = ft.Container(
                width=100,
                height=80,
                border_radius=12,
                bgcolor=bg,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(icone, color=cor, size=20),
                        ft.Text(nome, size=11)
                    ]
                )
            )

            def selecionar(e):
                categoria_selecionada["nome"] = nome
                for c in categorias_grid.controls:
                    c.border = None
                container.border = ft.border.all(2, cor)
                page.update()

            container.on_click = selecionar
            return container

        def atualizar_categorias():
            categorias_grid.controls.clear()
            categoria_selecionada["nome"] = None

            cats = ctrl_nova_transacao.buscar_categorias(tipo)

            for nome, icone, cor, bg in cats:
                categorias_grid.controls.append(
                    btn_categoria(nome, icone, cor, bg)
                )

            page.update()

        def mudar_tipo(novo_tipo):
            nonlocal tipo
            tipo = novo_tipo

            if tipo == "receita":
                toggle_receita.bgcolor = "#16A34A"
                toggle_receita.content = ft.Text("Receita", color="white")

            atualizar_categorias()

        toggle_receita = ft.Container(
            expand=True,
            height=40,
            border_radius=10,
            alignment=ft.Alignment(0, 0),
            bgcolor="#16A34A",
            content=ft.Text("Receita", color="white"),
            on_click=lambda e: mudar_tipo("receita")
        )
        mudar_tipo("receita")

        # =========================
        # SALVAR
        # =========================
        def salvar(e):
            def resetar_pagina(delay=0.5):
                time.sleep(delay)
                if self.on_save:
                    self.on_save()

            erros = []

            descricao = descricao_input.value.strip() if descricao_input.value else ""
            data = data_input.value.strip() if data_input.value else ""
            categoria = categoria_selecionada.get("nome")
            valor_float = converter_para_float(valor_input.value)

            if not descricao:
                erros.append("Descrição")

            if not data or len(data) < 10:
                erros.append("Data válida")

            if not categoria:
                erros.append("Categoria")

            if valor_float <= 0:
                erros.append("Valor maior que zero")

            if erros:
                mostrar_snackbar("Preencha: " + ", ".join(erros), "red")
                page.run_thread(lambda: resetar_pagina(2))
                return

            sucesso, erro = ctrl_nova_transacao.salvar_transacao(
                tipo=tipo,
                valor=valor_float,
                descricao=descricao,
                data=data,
                categoria=categoria,
                obs=obs_input.value
            )

            if sucesso:
                mostrar_snackbar(
                    f"Transação ({descricao}) salvo com sucesso!",
                    "green"
                )

                valor_input.value = "R$ 0,00"
                descricao_input.value = ""
                obs_input.value = ""
                categoria_selecionada["nome"] = None

                atualizar_categorias()

                page.run_thread(lambda: resetar_pagina(0.5))

            else:
                mostrar_snackbar(
                    erro if erro else "Erro ao salvar transação.",
                    "red"
                )
                page.run_thread(lambda: resetar_pagina(0.5))

            page.update()

        btn_salvar = ft.Container(
            height=50,
            border_radius=12,
            bgcolor=cor_tema_principal,
            alignment=ft.Alignment(0, 0),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.CupertinoIcons.CHECK_MARK, color="white"),
                    ft.Text(
                        "Salvar Transação",
                        color="white",
                        weight=ft.FontWeight.BOLD
                    )
                ]
            ),
            on_click=salvar
        )

        layout = ft.Container(
            padding=ft.padding.only(top=50, left=20, right=20),
            content=ft.Column(
                spacing=20,
                scroll=ft.ScrollMode.HIDDEN,
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                              icon=ft.CupertinoIcons.BACK,
                              on_click=lambda e: self.trocar_tela(0)
                            ),
                            ft.Text(
                                "Nova Receita",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            )
                        ]
                    ),
                    ft.Container(
                        padding=5,
                        border_radius=12,
                        bgcolor=cor_background_principal,
                        content=ft.Row(
                            controls=[toggle_receita]
                        )
                    ),
                    valor_input,
                    descricao_input,
                    data_input,
                    ft.Column(
                        controls=[
                            ft.Text("Categoria"),
                            categorias_grid
                        ]
                    ),
                    obs_input,
                    btn_salvar
                ]
            )
        )

        atualizar_categorias()

        return layout