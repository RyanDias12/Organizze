import flet as ft
from datetime import datetime

from src.views.style import *
from src.controllers.ctrl_metas import Ctrl_Metas


class Metas_View:
    def __init__(self, on_save=None, trocar_tela=None):

        self.on_save = on_save
        self.trocar_tela = trocar_tela

        self.ctrl_metas = Ctrl_Metas()

        self.lista_metas = ft.Column(
            spacing=15,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )

    # =========================================================
    # ATUALIZAR LISTA
    # =========================================================
    def atualizar_lista(self, page):

        self.lista_metas.controls.clear()

        metas = self.ctrl_metas.listar_meta()

        if not metas:

            self.lista_metas.controls.append(
                ft.Container(
                    padding=20,
                    border_radius=15,
                    bgcolor="white",
                    width=page.width,

                    content=ft.Text(
                        "Nenhuma meta cadastrada.",
                        text_align=ft.TextAlign.CENTER
                    )
                )
            )

        for meta in metas:

            progresso = 0

            if meta["valor_meta"] > 0:
                progresso = meta["valor_atual"] / meta["valor_meta"]

            card = ft.Container(
                padding=15,
                border_radius=20,
                bgcolor="white",

                content=ft.Column(
                    spacing=12,
                    controls=[

                        # ===================================
                        # TOPO
                        # ===================================
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                            controls=[

                                ft.Column(
                                    spacing=3,
                                    controls=[

                                        ft.Text(
                                            meta["descricao"],
                                            size=18,
                                            weight="bold"
                                        ),

                                        ft.Text(
                                            f"Prazo: {meta['data_limite']}",
                                            size=12,
                                            color="grey"
                                        ),
                                    ]
                                ),

                                ft.Row(
                                    controls=[

                                        # DEPOSITAR
                                        ft.IconButton(
                                            icon=ft.Icons.ADD_CIRCLE,
                                            icon_color="green",

                                            on_click=lambda e, m=meta:
                                            self.dialog_depositar(
                                                page,
                                                m
                                            )
                                        ),

                                        # EXCLUIR
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color="red",

                                            on_click=lambda e, id_meta=meta["id"]:
                                            self.excluir_meta(
                                                page,
                                                id_meta
                                            )
                                        ),
                                    ]
                                )
                            ]
                        ),

                        # ===================================
                        # BARRA
                        # ===================================
                        ft.ProgressBar(
                            value=progresso,
                            height=10,
                            color=cor_tema_principal,
                            bgcolor="#E5E7EB",
                        ),

                        # ===================================
                        # VALORES
                        # ===================================
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                            controls=[

                                ft.Text(
                                    f"Atual: R$ {meta['valor_atual']:.2f}",
                                    weight="bold"
                                ),

                                ft.Text(
                                    f"Meta: R$ {meta['valor_meta']:.2f}",
                                    weight="bold"
                                ),
                            ]
                        )
                    ]
                )
            )

            self.lista_metas.controls.append(card)

        page.update()

    # =========================================================
    # EXCLUIR META
    # =========================================================
    def excluir_meta(self, page, id_meta):

        sucesso, erro = self.ctrl_metas.delete_meta(id_meta)

        if sucesso:
            print("Meta deletada")

        else:
            print(erro)

        self.atualizar_lista(page)

    # =========================================================
    # DIALOG DE DEPOSITO
    # =========================================================
    def dialog_depositar(self, page, meta):

        def formatar_moeda(valor):

            numeros = "".join(filter(str.isdigit, valor))

            if numeros == "":
                return "R$ 0,00"

            numero = int(numeros) / 100

            return (
                f"R$ {numero:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        def on_change_valor(e):

            valor_limpo = "".join(
                filter(str.isdigit, e.control.value)
            )

            e.control.value = formatar_moeda(valor_limpo)

            e.control.update()

        valor_input = ft.TextField(
            label="Valor depósito",
            value="R$ 0,00",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=on_change_valor,
            focused_border_color=cor_tema_principal,
        )

        def confirmar(e):

            valor = (
                valor_input.value
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

            valor = float(valor)

            novo_valor = meta["valor_atual"] + valor

            self.ctrl_metas.update_meta(
                id_meta=meta["id"],
                valor_atual=novo_valor,
                valor_meta=meta["valor_meta"],
                descricao=meta["descricao"],
                data_limite=meta["data_limite"]
            )

            dialog.open = False

            self.atualizar_lista(page)

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=cor_background_principal,

            content=ft.Container(
                width=300,

                content=ft.Column(
                    tight=True,

                    controls=[

                        ft.Text(
                            "Adicionar valor",
                            size=20,
                            weight="bold"
                        ),

                        valor_input,

                        ft.ElevatedButton(
                            "Confirmar",
                            bgcolor=cor_tema_principal,
                            color="white",
                            on_click=confirmar
                        )
                    ]
                )
            )
        )

        page.overlay.append(dialog)

        dialog.open = True

        page.update()

    # =========================================================
    # DIALOG NOVA META
    # =========================================================
    def dialog_nova_meta(self, page):

        def formatar_moeda(valor):

            numeros = "".join(filter(str.isdigit, valor))

            if numeros == "":
                return "R$ 0,00"

            numero = int(numeros) / 100

            return (
                f"R$ {numero:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        def on_change_valor(e):

            valor_limpo = "".join(
                filter(str.isdigit, e.control.value)
            )

            e.control.value = formatar_moeda(valor_limpo)

            e.control.update()

        input_nome = ft.TextField(
            label="Nome da Meta",
            focused_border_color=cor_tema_principal,
        )

        input_data = ft.TextField(
            label="Prazo",
            value=datetime.now().strftime("%d/%m/%Y"),
            focused_border_color=cor_tema_principal,
        )

        input_valor = ft.TextField(
            label="Valor Meta",
            value="R$ 0,00",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=on_change_valor,
            focused_border_color=cor_tema_principal,
        )

        def salvar(e):

            valor = (
                input_valor.value
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

            valor = float(valor)

            self.ctrl_metas.criar_meta(
                valor_atual=0,
                valor_meta=valor,
                descricao=input_nome.value,
                data_criacao=datetime.now().strftime("%d/%m/%Y"),
                data_limite=input_data.value
            )

            dialog.open = False

            self.atualizar_lista(page)

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=cor_background_principal,

            content=ft.Container(
                width=300,

                content=ft.Column(
                    tight=True,
                    spacing=10,
                    controls=[

                        ft.Text(
                            "Nova Meta",
                            size=20,
                            weight="bold"
                        ),

                        input_nome,
                        input_data,
                        input_valor,

                        ft.ElevatedButton(
                            "Salvar",
                            bgcolor=cor_tema_principal,
                            color="white",
                            on_click=salvar
                        )
                    ]
                )
            )
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # =========================================================
    # PAGE
    # =========================================================
    def page(self, page: ft.Page):

        self.atualizar_lista(page)

        return ft.Container(
            expand=True,
            bgcolor=cor_background_principal,

            padding=ft.padding.only(
                top=50,
                left=20,
                right=20
            ),

            content=ft.Column(
                expand=True,
                spacing=20,
                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Text(
                                "Metas",
                                size=24,
                                weight="bold"
                            ),

                            ft.ElevatedButton(
                                "Nova Meta",
                                bgcolor=cor_tema_principal,
                                color=cor_background_principal,
                                on_click=lambda e:
                                self.dialog_nova_meta(page)
                            )
                        ]
                    ),

                    self.lista_metas
                ]
            )
        )