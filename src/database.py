import sqlite3
import os


class Database:
    def __init__(self):
        self.DB_FILE = "src/organizze.db"

    def iniciar_banco(self):
        if not os.path.exists(self.DB_FILE):
            print("Banco não existe. Criando...")
            conn = sqlite3.connect(self.DB_FILE)
            conn.close()
            print("Banco criado com sucesso!")
        else:
            print("Banco existe.")

    def conectar_db(self):
        try:
            return sqlite3.connect(self.DB_FILE)
        except Exception as e:
            print("Erro ao conectar:", e)
            return None

    #  TABELA CATEGORIA
    def criar_table_categoria(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                txt_icon TEXT,
                color_icon TEXT
            )
            """)
            conn.commit()
            print("Tabela categorias Criada com sucesso")
        except Exception as e:
            print(f"Erro : Falha ao Criar Tabela categorias.\n")
            print(f"Erro : {e}\n")
        finally:
            conn.close()

    # TABELA TRANSACAO
    def criar_table_transacao(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                descricao TEXT,
                data TEXT,
                categoria TEXT,
                observacao TEXT
            )
            """)
            conn.commit()
            print("Tabela transacoes Criada com sucesso")
        except Exception as e: 
            print("Erro : Falha ao Criar Tabela transacoes.\n")
            print(f"Erro : {e}\n")
        finally:
            conn.close()
            
    # TABELA TRANSACAO
    def criar_table_metas(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    valor_atual REAL NOT NULL,
                    valor_meta REAL NOT NULL,
                    descricao TEXT,
                    data_criacao TEXT,
                    data_limite TEXT
                )
            """)
            conn.commit()
            print("Tabela metas criada")
        except Exception as e:
            print("Erro tabela metas:", e)
        finally:
            conn.close()
            
    def criar_table_perfil(self):
        try:

            conn = self.conectar_db()

            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfil (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nome_usuario TEXT,

                nome TEXT,

                sobrenome TEXT,

                email TEXT UNIQUE,

                senha TEXT,

                nascimento TEXT,

                cor_tema TEXT
            )
            """)

            conn.commit()

            print("Tabela perfil criada")

        except Exception as e:

            print("Erro tabela perfil:", e)

        finally:

            conn.close()
                    
    def inserir_categorias_padrao(self):
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()

                categorias = [
                    # RECEITAS
                    ("Salário", "receita", "MONEY_DOLLAR", "#16A34A"),
                    ("Investimento", "receita", "CHART_BAR_ALT_FILL", "#0891B2"),
                    ("Freelance", "receita", "DESKTOPCOMPUTER", "#2563EB"),
                    ("Vendas", "receita", "TAG", "#7C3AED"),
                    ("Presente", "receita", "GIFT", "#DB2777"),
                    ("Cashback", "receita", "ARROW_UTURN_LEFT", "#059669"),
                    ("Outros", "receita", "ELLIPSIS", "#6B7280"),

                    # DESPESAS
                    ("Alimentação", "despesa", "FASTFOOD", "#F97316"),
                    ("Supermercado", "despesa", "SHOPPING_CART", "#EA580C"),
                    ("Restaurante", "despesa", "RESTAURANT", "#FB923C"),

                    ("Transporte", "despesa", "CAR", "#2563EB"),
                    ("Combustível", "despesa", "LOCAL_GAS_STATION", "#1D4ED8"),
                    ("Uber/Taxi", "despesa", "LOCATION_ON", "#3B82F6"),

                    ("Moradia", "despesa", "HOME", "#10B981"),
                    ("Aluguel", "despesa", "APARTMENT", "#059669"),
                    ("Condomínio", "despesa", "DOMAIN", "#047857"),

                    ("Contas", "despesa", "BOLT", "#EF4444"),
                    ("Energia", "despesa", "FLASH_ON", "#DC2626"),
                    ("Água", "despesa", "WATER_DROP", "#0EA5E9"),
                    ("Internet", "despesa", "WIFI", "#6366F1"),
                    ("Telefone", "despesa", "PHONE", "#8B5CF6"),

                    ("Saúde", "despesa", "HEART", "#EC4899"),
                    ("Farmácia", "despesa", "MEDICAL_SERVICES", "#F472B6"),
                    ("Academia", "despesa", "FITNESS_CENTER", "#BE185D"),

                    ("Educação", "despesa", "SCHOOL", "#F59E0B"),
                    ("Cursos", "despesa", "MENU_BOOK", "#D97706"),

                    ("Lazer", "despesa", "SPORTS_ESPORTS", "#8B5CF6"),
                    ("Viagem", "despesa", "FLIGHT", "#0EA5E9"),
                    ("Streaming", "despesa", "PLAY_CIRCLE", "#DC2626"),

                    ("Roupas", "despesa", "CHECKROOM", "#DB2777"),
                    ("Beleza", "despesa", "CONTENT_CUT", "#F472B6"),
                    ("Pets", "despesa", "PETS", "#A16207"),

                    ("Impostos", "despesa", "DESCRIPTION", "#374151"),
                    ("Investimentos", "despesa", "INSERT_CHART", "#0891B2"),

                    ("Outros", "despesa", "ELLIPSIS", "#6B7280"),
                ]

                for cat in categorias:
                    # evita duplicar
                    cursor.execute("""
                        SELECT COUNT(*) FROM categorias 
                        WHERE nome=? AND tipo=?
                    """, (cat[0], cat[1]))

                    if cursor.fetchone()[0] == 0:
                        cursor.execute("""
                            INSERT INTO categorias (nome, tipo, txt_icon, color_icon)
                            VALUES (?, ?, ?, ?)
                        """, cat)

                conn.commit()
                print("Categorias padrão inseridas com sucesso!")

            except Exception as e:
                print("Erro ao inserir categorias:", e)

            finally:
                conn.close()

    def tabela_existe(self, table_name):
        conn = self.conectar_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (table_name,)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None
            
    def inicia_app_db(self):
        self.iniciar_banco()
        
        categorias = self.tabela_existe("categorias")
        transacoes = self.tabela_existe("transacoes")
        metas = self.tabela_existe("metas")
    
        if categorias and transacoes and metas:
            print("As tabelas existem.")
        else:
            print("As tabelas NÃO existem.")
            # CRIAÇÃO TABLE
            self.criar_table_categoria()
            self.criar_table_transacao()
            self.criar_table_metas()
            self.criar_table_perfil()
            
            # INSERIR AUTOMATICO DB
            self.inserir_categorias_padrao()
