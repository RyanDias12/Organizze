import flet as ft

from src.views.style import *
from src.controllers.ctrl_auth import Ctrl_Auth


class Login_View:

    def __init__(
        self,
        entrar_app,
        abrir_cadastro,
        abrir_esqueci_senha
    ):

        self.ctrl = Ctrl_Auth()

        self.entrar_app = entrar_app

        self.abrir_cadastro = abrir_cadastro

        self.abrir_esqueci_senha = abrir_esqueci_senha

    def page(self, page: ft.Page):

        input_usuario = ft.TextField(
            label="Usuário",
            prefix_icon=ft.Icons.PERSON,
            focused_border_color=cor_tema_principal,
            filled=True,
            bgcolor="white"
        )

        input_senha = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            focused_border_color=cor_tema_principal,
            filled=True,
            bgcolor="white"
        )

        aviso = ft.Text(
            color="red",
            size=14
        )

        def fazer_login(e):

            usuario = input_usuario.value.strip()

            senha = input_senha.value.strip()

            if usuario == "" or senha == "":

                aviso.value = "Preencha usuário e senha"

                page.update()

                return

            perfil = self.ctrl.fazer_login(
                usuario,
                senha
            )

            if perfil:

                aviso.value = ""

                self.entrar_app()

            else:

                aviso.value = "Usuário ou senha inválidos"

                page.update()

        return ft.Container(
            expand=True,

            bgcolor=cor_background_principal,

            alignment=ft.Alignment(0, 0),

            content=ft.Container(
                width=350,

                padding=30,

                border_radius=25,

                bgcolor="white",

                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.BLACK12,
                    offset=ft.Offset(0, 4)
                ),

                content=ft.Column(
                    tight=True,

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    spacing=20,

                    controls=[

                        ft.Icon(
                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                            size=80,
                            color=cor_tema_principal
                        ),

                        ft.Text(
                            "Organizze",
                            size=30,
                            weight="bold",
                            text_align=ft.TextAlign.CENTER
                        ),

                        ft.Text(
                            "Controle financeiro inteligente",
                            size=14,
                            color=cor_text_aux,
                            text_align=ft.TextAlign.CENTER
                        ),

                        input_usuario,

                        input_senha,

                        aviso,

                        ft.ElevatedButton(
                            "Entrar",

                            width=300,

                            height=50,

                            bgcolor=cor_tema_principal,

                            color="white",

                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=12
                                )
                            ),

                            on_click=fazer_login
                        ),

                        ft.TextButton(
                            "Esqueci minha senha",

                            on_click=lambda e:
                            self.abrir_esqueci_senha()
                        ),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,

                            controls=[

                                ft.Text(
                                    "Não possui conta?"
                                ),

                                ft.TextButton(
                                    "Criar conta",

                                    on_click=lambda e:
                                    self.abrir_cadastro()
                                )
                            ]
                        )
                    ]
                )
            )
        )