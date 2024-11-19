import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from datetime import datetime

# Inicializar Firebase com apiKey e Storage Bucket
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\ddavi\\OneDrive\\Área de Trabalho\\work\\StoreFlet\\shop\\try1-d5f52-firebase-adminsdk-ox7ry-47c129a44d.json")

    firebase_admin.initialize_app(cred, {
        'apiKey': "AIzaSyCtAsNefm5FzL3bLMENYjAWxrqjiYqktZM",
        'storageBucket': 'try1-d5f52.appspot.com'
    })

db = firestore.client()
bucket = storage.bucket()

# Configurações de cores
PRIMARY_COLOR = "#000000"    # Preto
SECONDARY_COLOR = "#FFFFFF"  # Branco
TEXT_COLOR = "#FFFFFF"       # Branco

# Tela de Registro
class RegisterPage(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(RegisterPage, self).__init__(route="/register")
        self.page = page
        self.iniciar()

    def iniciar(self):
        self.page.bgcolor = PRIMARY_COLOR
        self.page.update()

        self.name_input = ft.TextField(label="Nome", width=280, bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR, text_size=16)
        self.email_input = ft.TextField(label="Email", width=280, bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR, text_size=16)
        self.password_input = ft.TextField(
            label="Senha", width=280, bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR, password=True, text_size=16
        )
        self.confirm_password_input = ft.TextField(
            label="Confirmar Senha", width=280, bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR, password=True, text_size=16
        )
        def handle_date_change(e):
            text = e.control.value  # Obtém o texto atual
            if len(text) == 2 and not text.endswith("/"):  # Após DD
                e.control.value += "/"
            elif len(text) == 5 and text.count("/") == 1:  # Após MM
                e.control.value += "/"
            e.control.update()

        self.birthdate_input = ft.TextField(
            label="Data de Nascimento (DD/MM/AAAA)",
            width=280,
            bgcolor=SECONDARY_COLOR,
            color=PRIMARY_COLOR,
            text_size=16,
            on_change=handle_date_change,  # Define o evento para detecção de mudanças
        )
        self.error_message = ft.Text(color=SECONDARY_COLOR, text_align="center")

        self.controls = [
            ft.Column(
                [
                    ft.Text("Registro", size=28, weight="bold", color=TEXT_COLOR, text_align="center"),
                    ft.Divider(height=20, color="transparent"),
                    self.name_input,
                    self.email_input,
                    self.password_input,
                    self.confirm_password_input,
                    self.birthdate_input,
                    ft.Divider(height=10, color="transparent"),
                    self.error_message,
                    ft.Divider(height=20, color="transparent"),
                    ft.ElevatedButton(
                        "Registrar",
                        width=150,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.WHITE, color=PRIMARY_COLOR, shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=self.registrar_usuario,
                    ),
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
        ]

    def registrar_usuario(self, e):
        nome = self.name_input.value
        email = self.email_input.value
        senha = self.password_input.value
        confirmacao_senha = self.confirm_password_input.value
        nascimento = self.birthdate_input.value

        # Validações
        if not nome or not email or not senha or not confirmacao_senha or not nascimento:
            self.error_message.value = "Todos os campos são obrigatórios."
            self.page.update()
            return

        if senha != confirmacao_senha:
            self.error_message.value = "As senhas não coincidem."
            self.page.update()
            return

        try:
            datetime.strptime(nascimento, "%d/%m/%Y")
        except ValueError:
            self.error_message.value = "Data de nascimento inválida. Use o formato DD/MM/AAAA."
            self.page.update()
            return

        # Salvar no Firebase
        try:
            user = auth.create_user(email=email, password=senha)
            db.collection('usuarios').document(user.uid).set({
                "nome": nome,
                "email": email,
                "nascimento": nascimento,
            })
            self.error_message.value = "Registro bem-sucedido! Redirecionando para o login..."
            self.page.update()
            self.page.go("/auth")
        except Exception as err:
            self.error_message.value = f"Erro ao registrar: {err}"
            self.page.update()


# Tela de Login
class AuthPage(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(AuthPage, self).__init__(route="/auth")
        self.page = page
        self.iniciar()

    def iniciar(self):
        self.page.bgcolor = PRIMARY_COLOR
        self.page.update()

        self.email_input = ft.TextField(label="Email", width=280, bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR, text_size=16)
        self.password_input = ft.TextField(
            label="Senha", width=280, bgcolor=SECONDARY_COLOR, color=PRIMARY_COLOR, password=True, text_size=16
        )
        self.error_message = ft.Text(color=SECONDARY_COLOR, text_align="center")

        self.controls = [
            ft.Column(
                [
                    ft.Text("Bem-Vindo", size=28, weight="bold", color=TEXT_COLOR, text_align="center"),
                    ft.Text("Login ou Registro", size=16, color=TEXT_COLOR, text_align="center"),
                    ft.Divider(height=20, color="transparent"),
                    self.email_input,
                    self.password_input,
                    ft.Divider(height=10, color="transparent"),
                    self.error_message,
                    ft.Divider(height=20, color="transparent"),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Login",
                                width=130,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.WHITE, color=PRIMARY_COLOR, shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=self.fazer_login,
                            ),
                            ft.ElevatedButton(
                                "Registrar",
                                width=130,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.WHITE, color=PRIMARY_COLOR, shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=lambda _: self.page.go("/register"),
                            ),
                        ],
                        alignment="center",
                        spacing=20,
                    ),
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
        ]

    def fazer_login(self, e):
        email = self.email_input.value
        password = self.password_input.value

        if not email or not password:
            self.error_message.value = "Preencha todos os campos."
            self.page.update()
            return

        try:
            user = auth.get_user_by_email(email)
            if user:
                global logged_in_user
                logged_in_user = user.uid
                self.page.go("/")
            else:
                self.error_message.value = "Usuário ou senha inválidos."
        except Exception as err:
            self.error_message.value = f"Erro ao logar: {err}"
        self.page.update()


# Página Inicial (Home)
class HomePage(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(HomePage, self).__init__(route="/")
        self.page = page
        self.user_name = None  # Nome do usuário logado
        self.produtos = []  # Lista de produtos
        self.busca_texto = ""  # Texto para busca
        self.iniciar()

    def iniciar(self):
        self.page.bgcolor = PRIMARY_COLOR
        self.page.update()

        self.bem_vindo_text = ft.Text(
            value=f"Bem-vindo, {self.user_name}!",
            size=28,
            weight="bold",
            color=TEXT_COLOR,
            text_align="center",
        )

        self.search_input = ft.TextField(
            hint_text="Buscar produtos...",
            width=300,
            bgcolor=SECONDARY_COLOR,
            color=PRIMARY_COLOR,
            on_change=self.buscar_produto,
        )

        self.produtos_container = ft.Column(
            spacing=10,
            alignment="center",
            controls=self.exibir_produtos(),
        )

        self.controls = [
            ft.Column(
                [
                    self.bem_vindo_text,
                    ft.Divider(height=10, color="transparent"),
                    self.search_input,
                    ft.Divider(height=10, color="transparent"),
                    ft.Text("Produtos disponíveis:", size=18, color=TEXT_COLOR, text_align="center"),
                    ft.Divider(height=10, color="transparent"),
                    self.produtos_container,
                    ft.Divider(height=20, color="transparent"),
                    ft.ElevatedButton(
                        "Adicionar Produto",
                        width=200,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.WHITE, color=PRIMARY_COLOR, shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=self.abrir_painel_adicionar_produto,
                    ),
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
        ]

    def exibir_produtos(self):
        produtos = Model.get_produtos()  # Busca produtos do Firebase
        produtos_lista = []

        # Filtro de busca
        for produto_id, values in produtos.items():
            if self.busca_texto.lower() in values.get("nome", "").lower():
                produto_card = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(values.get("nome", "Produto sem nome"), size=18, color=SECONDARY_COLOR),
                            ft.Text(f"R$ {values.get('preco', '0.00')}", size=16, color=SECONDARY_COLOR),
                            ft.Text(values.get("descricao", ""), size=14, color=SECONDARY_COLOR),
                        ]
                    ),
                    padding=10,
                    margin=5,
                    bgcolor="#202020",
                    border_radius=8,
                    alignment="center",
                    expand=True,
                )
                produtos_lista.append(produto_card)
        return produtos_lista

    def buscar_produto(self, e):
        self.busca_texto = e.control.value  # Atualiza o texto da busca
        self.produtos_container.controls = self.exibir_produtos()
        self.page.update()

    def abrir_painel_adicionar_produto(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Adicionar Produto"),
            content=PainelAdicionarProduto(self.page),
            actions=[
                ft.TextButton("Fechar", on_click=lambda _: self.page.dialog.close()),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def carregar_dados_usuario(self, user_id):
        try:
            usuario_doc = db.collection("usuarios").document(user_id).get()
            if usuario_doc.exists:
                self.user_name = usuario_doc.to_dict().get("nome", "Usuário")
            else:
                self.user_name = "Usuário"
        except Exception as e:
            print(f"Erro ao buscar dados do usuário: {e}")
            self.user_name = "Usuário"

    def atualizar_home(self, user_id):
        self.carregar_dados_usuario(user_id)
        self.bem_vindo_text.value = f"Bem-vindo, {self.user_name}!"
        self.produtos_container.controls = self.exibir_produtos()
        self.page.update()


# Painel para adicionar produtos
class PainelAdicionarProduto(ft.UserControl):
    def __init__(self, page: ft.Page) -> None:
        super(PainelAdicionarProduto, self).__init__()
        self.page = page

    def build(self):
        self.nome_input = ft.TextField(label="Nome do Produto", width=300)
        self.preco_input = ft.TextField(label="Preço", width=300)
        self.descricao_input = ft.TextField(label="Descrição", width=300)
        self.img_src_input = ft.TextField(label="URL da Imagem", width=300)
        self.error_message = ft.Text(color="red", size=14)

        return ft.Column(
            [
                self.nome_input,
                self.preco_input,
                self.descricao_input,
                self.img_src_input,
                self.error_message,
                ft.ElevatedButton(
                    "Salvar Produto",
                    width=150,
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.WHITE, color=PRIMARY_COLOR, shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    on_click=self.salvar_produto,
                ),
            ],
            alignment="start",
            spacing=10,
        )

    def salvar_produto(self, e):
        nome = self.nome_input.value
        preco = self.preco_input.value
        descricao = self.descricao_input.value
        img_src = self.img_src_input.value

        if not nome or not preco:
            self.error_message.value = "Nome e preço são obrigatórios!"
            self.update()
            return

        try:
            db.collection("produtos").add(
                {
                    "nome": nome,
                    "preco": preco,
                    "descricao": descricao,
                    "img_src": img_src,
                }
            )
            self.error_message.value = "Produto adicionado com sucesso!"
            self.update()
            self.page.dialog.close()
        except Exception as err:
            self.error_message.value = f"Erro ao salvar: {err}"
            self.update()



class ProfilePage(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(ProfilePage, self).__init__(route="/profile")
        self.page = page
        self.iniciar()

    def iniciar(self):
        self.page.bgcolor = PRIMARY_COLOR
        self.page.update()

        self.nome_input = ft.TextField(
            label="Alterar Nome",
            width=300,
            bgcolor=SECONDARY_COLOR,
            color=PRIMARY_COLOR,
        )

        self.profile_pic = ft.Image(
            src="",  # Padrão vazio
            width=100,
            height=100,
            border_radius=50,
            fit="cover",
        )

        self.controls = [
            ft.Column(
                [
                    self.profile_pic,
                    self.nome_input,
                    ft.ElevatedButton(
                        "Salvar Alterações",
                        on_click=self.salvar_alteracoes,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.WHITE, color=PRIMARY_COLOR, shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                    ),
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
        ]

    def salvar_alteracoes(self, e):
        nome = self.nome_input.value
        if nome:
            try:
                db.collection("usuarios").document(logged_in_user).update({"nome": nome})
                self.page.go("/")
            except Exception as err:
                print(f"Erro ao salvar alterações: {err}")


class Model:
    @staticmethod
    def get_produtos():
        try:
            produtos_ref = db.collection("produtos")
            produtos = produtos_ref.stream()
            return {
                produto.id: produto.to_dict()
                for produto in produtos
            }
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return {}






def main(page: ft.Page):
    global logged_in_user
    logged_in_user = None

    def router(route):
        page.views.clear()
        if not logged_in_user and page.route not in ["/auth", "/register"]:
            page.go("/auth")
        elif page.route == "/auth":
            page.views.append(AuthPage(page))
        elif page.route == "/register":
            page.views.append(RegisterPage(page))
        elif page.route == "/":
            home_page = HomePage(page)
            home_page.atualizar_home(logged_in_user)
            page.views.append(home_page)
        page.update()

    page.on_route_change = router
    page.go("/")



ft.app(target=main, assets_dir="assets")