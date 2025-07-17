class ControleVendedor:
    def __init__(self, controle_dados):
        self.vendedores = controle_dados.get_vendedores()

    def listar_vendedor(self):
        return [str(vendedor) for vendedor in self.vendedores]

    def adicionar_vendedor(self, vendedor):
        self.vendedores.append(vendedor)

    def buscar_vendedor_por_cpf(self, cpf):
        for vendedor in self.vendedores:
            if vendedor.get_cpf() == cpf:
                return vendedor
        return None

    def atualizar_vendedor(self, cpf, novos_dados):
        vendedor = self.buscar_vendedor_por_cpf(cpf)
        if vendedor:
            for chave, valor in novos_dados.items():
                setattr(vendedor, chave, valor)
            return vendedor
        return None

    def deletar_vendedor(self, cpf):
        vendedor = self.buscar_vendedor_por_cpf(cpf)
        if vendedor:
            self.vendedores.remove(vendedor)
            return True
        return False