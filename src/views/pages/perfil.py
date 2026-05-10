import flet as ft
from datetime import datetime
from src.views.style import *
from src.controllers.ctrl_perfil import Ctrl_Perfil


class Perfil_View:

    def __init__(self, on_save=None, trocar_tela=None):

        self.on_save = on_save
        self.trocar_tela = trocar_tela

        self.ctrl = Ctrl_Perfil()

    # =========================================================
    # INPUT PADRÃO MODERNO
    # =========================================================
    def input_padrao(self, label, value=None):

        return ft.TextField(
            label=label,
            value=value,

            text_size=15,

            border_radius=16,

            border_color="#E5E7EB",
            focused_border_color=cor_tema_principal,

            focused_border_width=2,

            filled=True,

            bgcolor="#FFFFFF",

            content_padding=18,

            cursor_color=cor_tema_principal,

            label_style=ft.TextStyle(
                size=13,
                color="#6B7280",
                weight=ft.FontWeight.W_500
            ),

            text_style=ft.TextStyle(
                size=15,
                color="#111827",
                weight=ft.FontWeight.W_500
            ),
        )

    # =========================================================
    # CARD INFO
    # =========================================================
    def card_info(self, titulo, valor, cor="#FFFFFF"):

        return ft.Container(
            expand=True,
            height=110,

            border_radius=20,
            bgcolor=cor,

            padding=15,

            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Text(
                        titulo,
                        size=13,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER
                    ),

                    ft.Text(
                        valor,
                        size=22,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            )
        )

    # =========================================================
    # PAGE
    # =========================================================
    def page(self, page: ft.Page):

        # =====================================================
        # CARREGAR PERFIL
        # =====================================================
        perfil = self.ctrl.carregar_perfil()

        nome = ""
        sobrenome = ""
        nascimento = ""
        email = ""
        cor_tema = "Verde"

        if perfil:

            nome = perfil.get("nome", "")
            sobrenome = perfil.get("sobrenome", "")
            nascimento = perfil.get("nascimento", "")
            email = perfil.get("email", "")
            cor_tema = perfil.get("cor_tema", "Verde")

        # =====================================================
        # INPUTS
        # =====================================================
        input_nome = self.input_padrao(
            "Nome",
            nome
        )

        input_sobrenome = self.input_padrao(
            "Sobrenome",
            sobrenome
        )

        input_data = self.input_padrao(
            "Data nascimento",
            nascimento
        )

        input_email = self.input_padrao(
            "E-mail",
            email
        )

        input_email.keyboard_type = ft.KeyboardType.EMAIL

        tema_dropdown = ft.Dropdown(
        label="Cor principal do layout",
        width=page.width,
        value=cor_tema,

        options=[
            ft.dropdown.Option("Azul"),
            ft.dropdown.Option("Verde"),
            ft.dropdown.Option("Roxo"),
            ft.dropdown.Option("Vermelho"),
            ft.dropdown.Option("Laranja"),
        ],

        border_radius=16,

        filled=True,

        bgcolor="#FFFFFF",

        border_color="#E5E7EB",

        focused_border_color=cor_tema_principal,

        focused_border_width=2,

        content_padding=18,

        label_style=ft.TextStyle(
            size=13,
            color="#6B7280",
            weight=ft.FontWeight.W_500
        ),

        text_style=ft.TextStyle(
            size=15,
            color="#111827",
            weight=ft.FontWeight.W_500
        ),
    )
        # =====================================================
        # AVISO
        # =====================================================
        aviso = ft.Text(
            "",
            color="green",
            size=14
        )

        # =====================================================
        # SALVAR PERFIL
        # =====================================================
        def salvar_perfil(e):

            self.ctrl.salvar_perfil(
                nome=input_nome.value,
                sobrenome=input_sobrenome.value,
                nascimento=input_data.value,
                email=input_email.value,
                cor_tema=tema_dropdown.value
            )

            aviso.value = "Perfil salvo com sucesso! - Reinicie o App para aplicar o tema."

            page.update()

        # =====================================================
        # DADOS FINANCEIROS
        # =====================================================
        total_transacoes = self.ctrl.total_transacoes()

        total_entrada = self.ctrl.total_entradas()

        total_saida = self.ctrl.total_saidas()

        saldo_total = self.ctrl.saldo_total()

        metas_atingidas = self.ctrl.metas_atingidas()

        total_metas = self.ctrl.total_metas()

        media_gastos = self.ctrl.media_gastos()

        economia_total = self.ctrl.economia_total()

        # =====================================================
        # BALANÇO MENSAL
        # =====================================================
        balancos = self.ctrl.balanco_mensal()

        meses = ft.Column(
            spacing=10
        )

        balancos_ordenados = sorted(
            balancos.items(),
            key=lambda item: datetime.strptime(item[0], "%B %Y"),
            reverse=True,
        )
        for mes, dados in balancos_ordenados:

            saldo = dados["saldo"]

            positivo = saldo >= 0

            meses.controls.append(

                ft.Container(
                    border_radius=15,
                    padding=15,
                    bgcolor="white",

                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Column(
                                spacing=3,

                                controls=[

                                    ft.Text(
                                        mes,
                                        size=16,
                                        weight="bold"
                                    ),

                                    ft.Text(
                                        f"Entradas: R$ {dados['entrada']:,.2f}"
                                    ),

                                    ft.Text(
                                        f"Saídas: R$ {dados['saida']:,.2f}"
                                    ),
                                ]
                            ),

                            ft.Text(
                                f"R$ {saldo:,.2f}",
                                color="green" if positivo else "red",
                                weight="bold",
                                size=16
                            )
                        ]
                    )
                )
            )

        # =====================================================
        # BOTÃO SALVAR
        # =====================================================
        btn_salvar = ft.Container(
            height=55,

            border_radius=18,

            bgcolor=cor_tema_principal,

            alignment=ft.Alignment(0, 0),

            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.SAVE,
                        color="white"
                    ),

                    ft.Text(
                        "Salvar Alterações",
                        color="white",
                        weight="bold",
                        size=16
                    )
                ]
            ),

            on_click=salvar_perfil
        )

        # =====================================================
        # PAGE
        # =====================================================
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

                scroll=ft.ScrollMode.HIDDEN,

                spacing=20,

                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Text(
                                "Perfil",
                                size=28,
                                weight="bold"
                            ),

                            ft.Icon(
                                ft.Icons.PERSON,
                                size=35,
                                color=cor_tema_principal
                            )
                        ]
                    ),

                    ft.Container(
                        padding=20,

                        border_radius=25,

                        bgcolor="white",

                        content=ft.Column(
                            spacing=15,

                            controls=[

                                ft.Text(
                                    "Informações pessoais",
                                    size=20,
                                    weight="bold"
                                ),

                                input_nome,

                                input_sobrenome,

                                input_data,

                                input_email,

                                tema_dropdown,

                                btn_salvar,

                                aviso
                            ]
                        )
                    ),

                    ft.Text(
                        "Resumo financeiro",
                        size=22,
                        weight="bold"
                    ),

                    ft.Row(
                        spacing=15,

                        controls=[

                            self.card_info(
                                "Transações",
                                str(total_transacoes)
                            ),

                            self.card_info(
                                "Metas",
                                f"{metas_atingidas}/{total_metas}"
                            ),
                        ]
                    ),

                    ft.Row(
                        spacing=15,

                        controls=[

                            self.card_info(
                                "Entradas",
                                f"R$ {total_entrada:,.2f}"
                            ),

                            self.card_info(
                                "Saídas",
                                f"R$ {total_saida:,.2f}"
                            ),
                        ]
                    ),

                    ft.Row(
                        spacing=15,

                        controls=[

                            self.card_info(
                                "Saldo",
                                f"R$ {saldo_total:,.2f}"
                            ),

                            self.card_info(
                                "Economia",
                                f"R$ {economia_total:,.2f}"
                            ),
                        ]
                    ),

                    ft.Container(
                        padding=20,

                        border_radius=25,
                        width=page.width,
                        bgcolor="#FFFFFF",

                        content=ft.Column(
                            spacing=10,

                            controls=[

                                ft.Text(
                                    "Análise geral",
                                    size=20,
                                    weight="bold"
                                ),

                                ft.Text(
                                    f"""
• Total de transações: {total_transacoes}

• Média mensal de gastos: R$ {media_gastos:,.2f}

• Metas atingidas: {metas_atingidas}

• Economia acumulada: R$ {economia_total:,.2f}

• Resultado financeiro: R$ {saldo_total:,.2f}
                                    """
                                )
                            ]
                        )
                    ),

                    ft.Text(
                        "Resultados mensais",
                        size=22,
                        weight="bold"
                    ),

                    meses,

                    ft.Container(height=30)
                ]
            )
        )