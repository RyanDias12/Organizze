import flet as ft
from src.views.style import *

from src.views.pages.inicio import Inicio_view
from src.views.pages.transacoes import TransacoesView
from src.views.pages.nova_transacao import Nova_Transacao_view
from src.views.pages.metas import Metas_View
from src.views.pages.perfil import Perfil_View
from src.views.pages.pages_atalhos.nova_despesa import Nova_despesa_view
from src.views.pages.pages_atalhos.nova_receita import Nova_receita_view


class LayoutPage:

    def page(self, page: ft.Page):

        page.bgcolor = cor_background_principal
        conteudo = ft.Container(expand=True,bgcolor=cor_background_principal)
        selected_index = 0
        nav_items = []

        # 🔁 troca de tela
        def trocar_tela(index):
            nonlocal selected_index
            selected_index = index

            if index == 0:
                inicio_view = Inicio_view(on_ver_tudo=lambda: trocar_tela(1), trocar_tela=trocar_tela)
                conteudo.content = inicio_view.page(page)
            elif index == 1:
                transacoes_view = TransacoesView()
                conteudo.content = transacoes_view.page(page)
                transacoes_view.carregar(page)
            elif index == 2:
                nova_transacao = Nova_Transacao_view(on_save=lambda: trocar_tela(2), trocar_tela=trocar_tela)
                conteudo.content = nova_transacao.page(page)
            elif index == 3:
                meta_view = Metas_View(on_save=lambda: trocar_tela(3), trocar_tela=trocar_tela)
                conteudo.content = meta_view.page(page)
            elif index == 4:
                perfil_view = Perfil_View()
                conteudo.content = perfil_view.page(page)
            elif index == 5:
                nova_despesa = Nova_despesa_view(on_save=lambda: trocar_tela(2),trocar_tela=trocar_tela)
                conteudo.content =nova_despesa.page(page)
            elif index == 6:
                nova_receita = Nova_receita_view(on_save=lambda: trocar_tela(2),trocar_tela=trocar_tela)
                conteudo.content =nova_receita.page(page)

            atualizar_navbar()
            page.update()

        # 🎯 item navbar
        def nav_item(icone, label, index):
            icon = ft.Icon(icone, size=24)
            text = ft.Text(label, size=11)

            nav_items.append((icon, text, index))

            return ft.Container(
                on_click=lambda e: trocar_tela(index),
                padding=12,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    controls=[icon, text],
                ),
            )

        # 🎨 cores
        def atualizar_navbar():
            for icon, text, index in nav_items:
                if index == selected_index:
                    icon.color = cor_tema_principal
                    text.color = cor_tema_principal
                else:
                    icon.color = cor_text_aux
                    text.color = cor_text_aux

        # 📱 navbar 
        navbar = ft.Container(
            height=160,
            bgcolor=cor_background_principal,
            padding=ft.padding.symmetric(horizontal=20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    nav_item(ft.Icons.HOME, "Inicio", 0),
                    nav_item(ft.Icons.SWAP_HORIZ, "Transações", 1),
                    ft.Container(width=60),
                    nav_item(ft.Icons.PIE_CHART, "Metas", 3),
                    nav_item(ft.Icons.PERSON, "Perfil", 4),
                ],
            ),
        )

        # ➕ botão central
        fab = ft.Container(
            width=60,
            height=60,
            bgcolor=cor_tema_principal,
            border_radius=30,
            alignment=ft.Alignment(0, 0),
            content=ft.Icon(ft.Icons.ADD, color="white"),
            on_click=lambda e: trocar_tela(2),
            shadow=ft.BoxShadow(
                blur_radius=15,
                spread_radius=1,
                color=ft.Colors.BLACK26,
            ),
        )

        # 🧱 layout
        layout = ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        conteudo,
                        navbar,
                    ],
                ),
                ft.Container(
                    content=fab,
                    bottom=80,
                    left=0,
                    right=0,
                    alignment=ft.Alignment(0, 0),
                ),
            ],
        )

        # inicial
        inicio_view = Inicio_view(on_ver_tudo=lambda: trocar_tela(1),trocar_tela=trocar_tela)
        conteudo.content = inicio_view.page(page)
        atualizar_navbar()

        return layout