import flet as ft
from src.views.style import *
from src.controllers.ctrl_transacoes import CtrlTransacao


class TransacoesView:
    def __init__(self):
        self.ctrl = CtrlTransacao()
        self.tipo_filtro = "tudo"
        self.dados = []

    def abrir_dialog_observacao(self, page, descricao, observacao):

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=cor_background_principal,
            shape=ft.RoundedRectangleBorder(radius=20),

            title=ft.Text(
                f"OBS: {descricao}",
                size=18,
                weight="bold"
            ),

            content=ft.Container(
                width=300,
                padding=10,
                content=ft.Text(
                    observacao if observacao else "Sem observação",
                    size=14,
                    color=ft.Colors.BLACK_87,
                )
            ),

            actions=[
                ft.TextButton(
                    "Fechar",
                    on_click=lambda e: fechar_dialog()
                )
            ]
        )

        def fechar_dialog():
            dialog.open = False
            page.update()

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def criar_item(self, t, page):
        return ft.Container(
            padding=10,
            border_radius=12,
            bgcolor=cor_background_principal,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[

                    ft.Row(
                        controls=[
                            ft.Container(
                                width=50,
                                height=50,
                                border_radius=10,
                                bgcolor="#E5E7EB",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    t["icone"],
                                    size=30,
                                    color=t["cor_icon"],
                                )
                            ),

                            ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Container(
                                        padding=0,
                                        margin=0,
                                        ink=True,
                                        on_click=lambda e: self.abrir_dialog_observacao(
                                            e.page,
                                            t["descricao"],
                                            t["observacao"]
                                        ),
                                        content=ft.Text(
                                            t["descricao"],
                                            weight=ft.FontWeight.BOLD,
                                            color=cor_text_padrao,
                                            size=14
                                        )
                                    ),
                                    ft.Text(
                                        f'{t["categoria"]} • {t["data"]}',
                                        size=11,
                                        color="gray"
                                    )
                                ]
                            )
                        ]
                    ),

                    ft.Row(
                        controls=[
                            ft.Text(t["valor"], color=t["cor"], weight="bold"),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, id_=t["id"]: self.deletar(id_, page)
                            )
                        ]
                    )
                ]
            )
        )


    def agrupar_por_mes(self, dados):
        resultado = {}

        for t in dados:
            dt = t["data_raw"]

            if dt:
                chave = dt.strftime("%B %Y").capitalize()
                chave_ordem = (dt.year, dt.month)
            else:
                chave = "Sem data"
                chave_ordem = (0, 0)

            if chave not in resultado:
                resultado[chave] = {
                    "ordem": chave_ordem,
                    "dados": []
                }

            resultado[chave]["dados"].append(t)

        # 🔥 ordena por ano e mês
        ordenado = dict(
            sorted(
                resultado.items(),
                key=lambda item: item[1]["ordem"],
                reverse=True
            )
        )

        # remove campo auxiliar
        return {
            chave: valor["dados"]
            for chave, valor in ordenado.items()
        }

    def aplicar_filtros(self):
        texto = (self.busca.value or "").lower()

        filtrado = []

        for t in self.dados:
            if texto not in t["descricao"].lower():
                continue

            if self.tipo_filtro != "tudo" and t["tipo"] != self.tipo_filtro:
                continue

            filtrado.append(t)

        return filtrado

    def renderizar(self, page):
        self.lista.controls.clear()

        dados_filtrados = self.aplicar_filtros()
        agrupado = self.agrupar_por_mes(dados_filtrados)

        if not agrupado:
            self.lista.controls.append(
                ft.Text("Nenhuma transação encontrada")
            )
        else:
            for mes, transacoes in agrupado.items():

                self.lista.controls.append(
                    ft.Text(mes, size=14, weight="bold", color="gray")
                )

                for t in transacoes:
                    self.lista.controls.append(
                        self.criar_item(t, page)
                    )

        page.update()

    def carregar(self, page):
        self.dados = self.ctrl.buscar_transacoes()
        self.renderizar(page)

    def deletar(self, id_, page):
        self.ctrl.deletar(id_)
        self.carregar(page)

    def set_filtro(self, tipo, page):
        self.tipo_filtro = tipo
        self.renderizar(page)

    def buscar(self, e):
        self.renderizar(e.page)

    def page(self, page: ft.Page):

        self.busca = ft.TextField(
            hint_text="Buscar transação...",
            on_change=self.buscar,
            width=page.window.width
        )

        self.lista = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.HIDDEN,
            expand=True
        )

        filtros = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.TextButton("Tudo", on_click=lambda e: self.set_filtro("tudo", page)),
                ft.TextButton("Receitas", on_click=lambda e: self.set_filtro("receita", page)),
                ft.TextButton("Despesas", on_click=lambda e: self.set_filtro("despesa", page)),
            ]
        )

        return ft.Container(
            expand=True,
            padding=ft.padding.only(top=50, left=20, right=20),
            bgcolor=cor_background_principal,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text("Transações", size=22, weight="bold"),
                    self.busca,
                    filtros,
                    self.lista
                ]
            )
        )