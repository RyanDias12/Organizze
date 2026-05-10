import flet as ft

from src.views.style import *

from src.controllers.ctrl_auth import Ctrl_Auth


class EsqueciSenha_View:

    def __init__(self, voltar_login):

        self.ctrl = Ctrl_Auth()

        self.voltar_login = voltar_login

    def page(self, page: ft.Page):

        input_email = ft.TextField(
            label="Digite seu e-mail",

            prefix_icon=ft.Icons.EMAIL,

            focused_border_color=cor_tema_principal,

            filled=True,

            bgcolor="white"
        )

        resultado = ft.Text()

        def recuperar(e):

            senha = self.ctrl.recuperar_senha(
                input_email.value
            )

            if senha:

                resultado.value = f"Sua senha é: {senha}"

                resultado.color = "green"

            else:

                resultado.value = "E-mail não encontrado"

                resultado.color = "red"

            page.update()

        return ft.Container(
            expand=True,

            bgcolor=cor_background_principal,

            padding=30,

            content=ft.Column(
                spacing=20,

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.LOCK_RESET,
                        size=80,
                        color=cor_tema_principal
                    ),

                    ft.Text(
                        "Recuperar senha",
                        size=28,
                        weight="bold"
                    ),

                    ft.Text(
                        "Digite seu e-mail cadastrado",
                        color=cor_text_aux
                    ),

                    input_email,

                    ft.ElevatedButton(
                        "Recuperar senha",

                        width=250,

                        bgcolor=cor_tema_principal,

                        color="white",

                        on_click=recuperar
                    ),

                    resultado,

                    ft.TextButton(
                        "Voltar para login",

                        on_click=lambda e:
                        self.voltar_login()
                    )
                ]
            )
        )