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
PRIMARY_COLOR = "#000000"  # Preto
SECONDARY_COLOR = "#FFFFFF"  # Branco
TEXT_COLOR = "#FFFFFF"

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
                    ft.Text("Bem-vindo", size=28, weight="bold", color=TEXT_COLOR, text_align="center"),
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
        self.user_name = None  
        self.produtos = [] 
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

        self.produtos_container = ft.Column(
            spacing=10,
            alignment="center",
            controls=self.exibir_produtos(),
        )

        self.controls = [
            ft.Column(
                [
                    self.bem_vindo_text,
                    ft.Divider(height=20, color="transparent"),
                    ft.Text("Produtos disponíveis:", size=18, color=TEXT_COLOR, text_align="center"),
                    ft.Divider(height=10, color="transparent"),
                    self.produtos_container,
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True,
            )
        ]

    def exibir_produtos(self):
        produtos = Model.get_produtos()  # Busca produtos do Firebase
        produtos_lista = []
        for produto_id, values in produtos.items():
            produto_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(values.get("nome", "Produto sem nome"), size=18, color=SECONDARY_COLOR),
                        ft.Text(f"R$ {values.get('preco', '0.00')}", size=16, color=SECONDARY_COLOR),
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


# Atualização da lógica de navegação
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

