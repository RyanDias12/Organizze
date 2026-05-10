import flet as ft
import asyncio

from src.views.style import *
from src.controllers.ctrl_inicio import Ctrl_inicio
from src.controllers.ctrl_perfil import Ctrl_Perfil


class Inicio_view:

    def __init__(self, on_ver_tudo=None, trocar_tela=None):

        self.ctrl = Ctrl_inicio()

        self.on_ver_tudo = on_ver_tudo

        self.trocar_tela = trocar_tela

    # =====================================================
    # ITEM TRANSAÇÃO
    # =====================================================
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
                                width=40,
                                height=40,

                                border_radius=10,

                                bgcolor="#E5E7EB",

                                alignment=ft.Alignment(0, 0),

                                content=ft.Icon(
                                    t["icone"],
                                    size=20,
                                    color=t["cor_icon"],
                                )
                            ),

                            ft.Column(
                                spacing=2,

                                controls=[

                                    ft.Text(
                                        t["descricao"],
                                        weight="bold"
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

                    ft.Text(
                        t["valor"],
                        color=t["cor"],
                        weight="bold"
                    )
                ]
            )
        )

    # =====================================================
    # PAGE
    # =====================================================
    def page(self, page: ft.Page):

        barras_refs = []

        # =====================================================
        # CONTROLLERS
        # =====================================================
        ctrl_perfil = Ctrl_Perfil()

        # =====================================================
        # PERFIL
        # =====================================================
        perfil = ctrl_perfil.carregar_perfil()

        nome_usuario = "Usuário"

        if perfil:

            nome = perfil.get("nome", "")

            sobrenome = perfil.get("sobrenome", "")

            nome_usuario = f"{nome} {sobrenome}".strip()

        # =====================================================
        # TRANSAÇÕES
        # =====================================================
        transacoes = self.ctrl.buscar_transacoes()[:5]

        gastos_graficos = self.ctrl.buscar_gastos_por_categoria()

        resumo = self.ctrl.resumo_financeiro()

        lista_transacoes = [

            self.criar_item(t, page)

            for t in transacoes
        ]

        # =====================================================
        # BOTÃO ATALHO
        # =====================================================
        def botao_atalho(
            icone,
            cor_icone,
            cor_fundo,
            texto,
            on_click=None
        ):

            return ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                spacing=8,

                controls=[

                    ft.IconButton(
                        icon=icone,

                        icon_color=cor_icone,

                        icon_size=24,

                        style=ft.ButtonStyle(
                            bgcolor=cor_fundo,

                            shape=ft.RoundedRectangleBorder(
                                radius=18
                            ),

                            padding=15
                        ),

                        on_click=on_click
                        if on_click
                        else lambda e: print(f"Clicou em {texto}")
                    ),

                    ft.Text(
                        texto,
                        size=13,
                        color=cor_text_aux
                    )
                ]
            )

        # =====================================================
        # BARRA CATEGORIA
        # =====================================================
        def barra_categoria(
            nome,
            porcentagem,
            cor
        ):

            largura_total = page.width

            barra = ft.Container(
                width=0,

                height=8,

                border_radius=10,

                bgcolor=cor,

                animate=ft.Animation(
                    duration=1200,
                    curve=ft.AnimationCurve.EASE_OUT
                ),
            )

            barras_refs.append(
                (
                    barra,
                    (porcentagem / 100) * largura_total
                )
            )

            return ft.Column(
                spacing=5,

                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Text(
                                nome,
                                size=13,
                                color=cor_text_padrao
                            ),

                            ft.Text(
                                f"{porcentagem}%",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),
                        ]
                    ),

                    ft.Container(
                        width=largura_total,

                        height=8,

                        border_radius=10,

                        bgcolor=cor_background_principal,

                        clip_behavior=ft.ClipBehavior.HARD_EDGE,

                        content=ft.Stack(
                            controls=[
                                barra
                            ]
                        )
                    )
                ]
            )

        # =====================================================
        # ANIMAÇÃO
        # =====================================================
        async def animar_barras():

            await asyncio.sleep(0.1)

            for barra, largura in barras_refs:

                barra.width = largura

                barra.update()

                await asyncio.sleep(0.15)

        # =====================================================
        # TEXTOS
        # =====================================================
        saudacao = ft.Text(
            "Seja Bem-vindo,",
            color=cor_text_aux,
            weight=ft.FontWeight.BOLD,
            size=15
        )

        nome_user = ft.Text(
            nome_usuario,
            color=cor_text_padrao,
            weight=ft.FontWeight.BOLD,
            size=25
        )

        text_titulo = ft.Column(
            spacing=0,

            controls=[
                saudacao,
                nome_user
            ]
        )

        notificacao_btn = ft.IconButton(
            icon=ft.CupertinoIcons.BELL,

            icon_size=30,

            icon_color=cor_tema_principal,
        )

        valor_total_conta = ft.Text(
            f'R$ {resumo["saldo"]:.2f}',

            color=cor_background_principal,

            weight=ft.FontWeight.BOLD,

            size=30
        )

        visualizacao_on = ft.IconButton(
            icon=ft.CupertinoIcons.EYE,

            icon_color=cor_background_principal,

            icon_size=18
        )

        valor_total_receitas = ft.Text(
            f'R$ {resumo["receitas"]:.2f}',

            color=cor_background_principal,

            weight=ft.FontWeight.BOLD,

            size=16
        )

        valor_total_despesas = ft.Text(
            f'R$ {resumo["despesas"]:.2f}',

            color=cor_background_principal,

            weight=ft.FontWeight.BOLD,

            size=16
        )

        # =====================================================
        # BOTÕES
        # =====================================================
        btn_nova_receitas = botao_atalho(
            ft.CupertinoIcons.ARROW_UP_RIGHT,
            "#16A34A",
            "#DDF7E7",
            "Receita",
            on_click=lambda e: self.trocar_tela(6)
        )

        btn_nova_despesas = botao_atalho(
            ft.CupertinoIcons.ARROW_DOWN_RIGHT,
            "#EF4444",
            "#FBE4E6",
            "Despesa",
            on_click=lambda e: self.trocar_tela(5)
        )

        btn_historico = botao_atalho(
            ft.CupertinoIcons.ARROW_UP_ARROW_DOWN,
            "#2563EB",
            "#DEE8FF",
            "Histórico",
            on_click=lambda e:
            self.on_ver_tudo()
            if self.on_ver_tudo
            else None,
        )

        btn_orcamento = botao_atalho(
            ft.CupertinoIcons.CHART_PIE,
            "#9333EA",
            "#EFE2FF",
            "Metas",
            on_click=lambda e: self.trocar_tela(3)
        )

        # =====================================================
        # GRÁFICO
        # =====================================================
        if not gastos_graficos:

            grafico = ft.Text(
                "Sem dados de despesas ainda",
                color="gray"
            )

        else:

            grafico = ft.Column(
                controls=[

                    barra_categoria(
                        g["categoria"],
                        g["porcentagem"],
                        g["cor"]
                    )

                    for g in gastos_graficos
                ]
            )

        # =====================================================
        # LAYOUT
        # =====================================================
        layout = ft.Container(
            bgcolor=cor_background_principal,

            expand=True,

            padding=ft.padding.only(
                top=50,
                left=20,
                right=20
            ),

            content=ft.Column(
                spacing=20,

                scroll=ft.ScrollMode.HIDDEN,

                controls=[

                    # =========================================
                    # TOPO
                    # =========================================
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[
                            text_titulo,
                            notificacao_btn
                        ]
                    ),

                    # =========================================
                    # CARD SALDO
                    # =========================================
                    ft.Container(
                        height=160,

                        border_radius=20,

                        padding=ft.Padding.only(
                            left=20,
                            top=20,
                            right=20,
                            bottom=30
                        ),

                        bgcolor=cor_tema_principal,

                        content=ft.Column(
                            spacing=8,

                            controls=[

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                    controls=[

                                        ft.Column(
                                            spacing=0,

                                            controls=[

                                                ft.Text(
                                                    "Saldo Total",
                                                    color="white70",
                                                    size=15,
                                                    weight=ft.FontWeight.BOLD
                                                ),

                                                valor_total_conta,
                                            ]
                                        ),

                                        visualizacao_on
                                    ]
                                ),

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,

                                    controls=[

                                        ft.Column(
                                            spacing=0,

                                            controls=[

                                                ft.Text(
                                                    "RECEITA MENSAL",
                                                    color="white70",
                                                    size=11
                                                ),

                                                valor_total_receitas
                                            ]
                                        ),

                                        ft.Column(
                                            spacing=0,

                                            controls=[

                                                ft.Text(
                                                    "DESPESA MENSAL",
                                                    color="white70",
                                                    size=11
                                                ),

                                                valor_total_despesas
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ),

                    # =========================================
                    # BOTÕES
                    # =========================================
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[
                            btn_nova_receitas,
                            btn_nova_despesas,
                            btn_historico,
                            btn_orcamento,
                        ]
                    ),

                    # =========================================
                    # GRÁFICO
                    # =========================================
                    ft.Column(
                        spacing=15,

                        controls=[

                            ft.Text(
                                "Gastos Mensal por Categoria",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=cor_text_padrao
                            ),

                            grafico
                        ]
                    ),

                    # =========================================
                    # ÚLTIMAS TRANSAÇÕES
                    # =========================================
                    ft.Column(
                        spacing=15,

                        controls=[

                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Últimas Transações",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=cor_text_padrao
                                    ),

                                    ft.TextButton(
                                        "Ver tudo",

                                        on_click=lambda e:
                                        self.on_ver_tudo()
                                        if self.on_ver_tudo
                                        else None,

                                        style=ft.ButtonStyle(
                                            color=cor_tema_principal
                                        )
                                    )
                                ]
                            ),

                            *lista_transacoes
                        ]
                    )
                ]
            )
        )

        page.run_task(animar_barras)

        return layout