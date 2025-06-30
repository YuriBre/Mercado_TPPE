class ControleVenda:
    def __init__(self, controle_dados):
        self.vendas = controle_dados.get_vendas()

    def listar_vendas(self):
        return [str(venda) for venda in self.vendas]

    def adicionar_venda(self, venda):
        self.vendas.append(venda)

    def buscar_venda_por_id(self, id_venda):
        for venda in self.vendas:
            if venda.id == id_venda:
                return venda
        return None