class ControleCliente:
    def __init__(self, controle_dados):
        self.clientes = controle_dados.get_clientes()

    def listar_clientes(self):
        return [str(cliente) for cliente in self.clientes]

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def buscar_cliente_por_cpf(self, cpf):
        for cliente in self.clientes:
            if cliente.get_cpf() == cpf:
                return cliente
        return None

    def atualizar_cliente(self, cpf, novos_dados):
        cliente = self.buscar_cliente_por_cpf(cpf)
        if cliente:
            for chave, valor in novos_dados.items():
                setattr(cliente, chave, valor)
            return cliente
        return None

    def deletar_cliente(self, cpf):
        cliente = self.buscar_cliente_por_cpf(cpf)
        if cliente:
            self.clientes.remove(cliente)
            return True
        return False