import flet as ft

from src.database import Database

from src.views.layout.layout_page import LayoutPage

from src.views.login_view import Login_View

from src.views.cadastro_view import Cadastro_View

from src.views.esqueci_senha_view import EsqueciSenha_View


def main(page: ft.Page):

    # =====================================================
    # DATABASE
    # =====================================================
    db = Database()

    db.inicia_app_db()

    # =====================================================
    # PAGE CONFIG
    # =====================================================
    page.title = "Organizze"

    page.theme_mode = ft.ThemeMode.LIGHT

    page.padding = 0

    page.window.width = 400

    page.window.height = 700

    page.window.prevent_setting_unit_size = True

    # =====================================================
    # FUNÇÕES NAVEGAÇÃO
    # =====================================================

    # APP PRINCIPAL
    def abrir_app():

        page.clean()

        layout = LayoutPage()

        page.add(layout.page(page))

        page.update()

    # LOGIN
    def abrir_login():

        page.clean()

        login = Login_View(
            entrar_app=abrir_app,

            abrir_cadastro=abrir_cadastro,

            abrir_esqueci_senha=abrir_esqueci_senha
        )

        page.add(login.page(page))

        page.update()

    # CADASTRO
    def abrir_cadastro():

        page.clean()

        cadastro = Cadastro_View(
            voltar_login=abrir_login
        )

        page.add(cadastro.page(page))

        page.update()

    # ESQUECI SENHA
    def abrir_esqueci_senha():

        page.clean()

        esqueceu = EsqueciSenha_View(
            voltar_login=abrir_login
        )

        page.add(esqueceu.page(page))

        page.update()

    # =====================================================
    # INICIAR NO LOGIN
    # =====================================================

    abrir_login()


ft.run(main)