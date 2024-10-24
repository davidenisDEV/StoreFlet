import flet as ft


class LandPage(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(LandPage, self).__init__(
            route="/", horizontal_alignment="center",
            vertical_alignment="center"
        )
        
        self.page = page
        
        self.logo_carrinho_compras = ft.Icon(name="shopping_cart_outlined", size=64)
        self.titulo = ft.Text("Lojinha do Denis".upper(), size=28, weight="bold")
        self.subtitulo = ft.Text("Feito para teste com FLET", size=11)
        
        self.btn_pagina_prod = ft.IconButton(
            "arrow_forward",
            width=54,
            height=54,
            style=ft.ButtonStyle(
                bgcolor={"": "#202020"},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                side={"": ft.BorderSide(2, "white54")},
            ),
            on_click=lambda e: self.page.go("/produtos")
        )

        self.controls = [
            self.logo_carrinho_compras,
            ft.Divider(height=25, color="transparent"),
            self.titulo,
            self.subtitulo,
            ft.Divider(height=10, color="transparent"),
            self.btn_pagina_prod
        ]


class Model(object):
    produtos: dict = {
        0: {
            "id": "1",
            "img_src": "/assets/camisa.jpg",
            "nome": "Camiseta Estampada",
            "descricao": "Camiseta de algodão com estampa criativa.",
            "preco": "49.99",
        },
        1: {
            "id": "2",
            "img_src": "/assets/tenis.jpg",
            "nome": "Tênis Esportivo",
            "descricao": "Tênis confortável para corrida e uso diário.",
            "preco": "199.99",
        },
        2: {
            "id": "3",
            "img_src": "/assets/mochila.jpg",
            "nome": "Mochila de Couro",
            "descricao": "Mochila de couro premium com compartimentos espaçosos.",
            "preco": "299.99",
        },
        3: {
            "id": "4",
            "img_src": "/assets/relogio.jpg",
            "nome": "Relógio Clássico",
            "descricao": "Relógio de mesa com design elegante.",
            "preco": "399.99",
        },
        4: {
            "id": "5",
            "img_src": "/assets/fone.jpg",
            "nome": "Fone de Ouvido Bluetooth",
            "descricao": "Fone sem fio com cancelamento de ruído e som de alta qualidade.",
            "preco": "149.99",
        }
        
    }
    
    carrinho: dict = {}
    
    @staticmethod
    def get_produtos() -> dict:
        return Model.produtos
    
    @staticmethod
    def get_carrinho() -> dict:
        return Model.carrinho 


class Produto(ft.View):
    def __init__(self, page: ft.Page) -> None:
        super(Produto, self).__init__(route="/produtos")
        self.page = page
        self.iniciar()

    def iniciar(self):
        self.produtos = ft.Row(expand=True, scroll="auto", spacing=30)
        self.criar_produtos()

        self.controls = [
            self.display_produto_pagina_header(),
            ft.Text("Loja", size=32),
            ft.Text("Selecione o item da lista abaixo"),
            self.produtos,
            self.display_produto_pagina_footer(),
        ]
        
    def display_produto_pagina_footer(self):
        return ft.Row([ft.Text("Denis Loja", size=10)], alignment="center")
    
    def display_produto_pagina_header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon("settings", size=18),
                    ft.IconButton(
                        "shopping_cart_outlined",
                        on_click=lambda e: self.page.go("/carrinho"),
                        icon_size=18,
                    )
                ],
                alignment="spaceBetween"
            )
        )

    def criar_produtos(self, produtos: dict = Model.get_produtos()) -> None:
        for _, values in produtos.items():
            for key, value in values.items():
                if key == "img_src":
                    img_src = self.criar_produto_img(img_path=value)

                elif key == "nome":
                    nome = values["nome"]

                elif key == "descricao":
                    descricao = values["descricao"]

                elif key == "id":
                    idd = values["id"]

                elif key == "preco":
                    preco = self.criar_produto_evento(values["preco"], idd)

            texts = self.criar_produto_texto(nome, descricao)
            self.criar_visualizacao_item(img_src, texts, preco)

    def criar_visualizacao_item(self, img_src, texts, preco):
        item = ft.Column()

        item.controls.append(self.criar_produto_container(5, img_src))
        item.controls.append(self.criar_produto_container(5, texts))
        item.controls.append(self.criar_produto_container(1, preco))

        self.produtos.controls.append(self.criar_item_wraper(item))

    def criar_item_wraper(self, item: ft.Column):
        return ft.Container(
            width=250,
            height=450,
            content=item,
            padding=8,
            border_radius=6
        )

    def criar_produto_img(self, img_path: str):
        return ft.Container(
            image=ft.Image(src=img_path, fit="fill"),
            border_radius=6, padding=10
        )

    def criar_produto_texto(self, nome: str, descricao: str):
        return ft.Column([ft.Text(nome, size=18), ft.Text(descricao, size=11)])

    def criar_produto_evento(self, preco: str, idd: str):
        return ft.Row(
            [
                ft.Text(preco, size=14),
                ft.IconButton(
                    "adicionar", data=idd,
                    # on_click=self.adc_ao_carrinho
                )
            ],
            alignment="spaceBetween"
        )

    def criar_produto_container(self, expand: bool, control: ft.Control):
        return ft.Container(content=control, expand=expand, padding=5)


def main(page: ft.Page) -> None:
    
    def router(route) -> None:
        page.views.clear()
        
        if page.route == "/":
            landing = LandPage(page)
            page.views.append(landing)
        
        elif page.route == "/produtos":
            produtos = Produto(page)
            page.views.append(produtos)
        
        page.update()
    
    page.on_route_change = router
    page.go("/")


ft.app(target=main, assets_dir="assets")
