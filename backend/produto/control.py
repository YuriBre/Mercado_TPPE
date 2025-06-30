class ControleProduto:
    def __init__(self, controle_dados):
        self.produtos = controle_dados.get_produtos()

    def listar_produtos(self):
        return [str(produto) for produto in self.produtos]

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def buscar_produto_por_id(self, id_produto):
        for produto in self.produtos:
            if produto.id == id_produto:
                return produto
        return None