import flet as ft

from src.views.style import *
from src.controllers.ctrl_auth import Ctrl_Auth


class Cadastro_View:

    def __init__(self, voltar_login):

        self.ctrl = Ctrl_Auth()

        self.voltar_login = voltar_login

    def page(self, page: ft.Page):

        nome_usuario = ft.TextField(label="Usuário")

        nome = ft.TextField(label="Nome")

        sobrenome = ft.TextField(label="Sobrenome")

        email = ft.TextField(label="E-mail")

        senha = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True
        )

        nascimento = ft.TextField(
            label="Nascimento"
        )

        aviso = ft.Text(color="red")

        def cadastrar(e):

            sucesso, erro = self.ctrl.cadastrar(
                nome_usuario.value,
                nome.value,
                sobrenome.value,
                email.value,
                senha.value,
                nascimento.value,
                "Verde"
            )

            if sucesso:

                self.voltar_login()

            else:

                aviso.value = erro

                page.update()

        return ft.Container(
            expand=True,
            padding=30,
            bgcolor=cor_background_principal,

            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=15,

                controls=[

                    ft.Text(
                        "Criar conta",
                        size=28,
                        weight="bold"
                    ),

                    nome_usuario,
                    nome,
                    sobrenome,
                    email,
                    senha,
                    nascimento,

                    aviso,

                    ft.ElevatedButton(
                        "Cadastrar",
                        bgcolor=cor_tema_principal,
                        color="white",
                        on_click=cadastrar
                    )
                ]
            )
        )