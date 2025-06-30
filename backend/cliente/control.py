class ControleCliente:
    def __init__(self, controle_dados):
        self.clientes = controle_dados.get_clientes()

    def listar_clientes(self):
        return [str(cliente) for cliente in self.clientes]

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def buscar_cliente_por_id(self, id):
        for cliente in self.clientes:
            if cliente.get_id() == id:
                return cliente
        return None

    def atualizar_cliente(self, id, novos_dados):
        cliente = self.buscar_cliente_por_id(id)
        if cliente:
            for chave, valor in novos_dados.items():
                setattr(cliente, chave, valor)
            return cliente
        return None

    def deletar_cliente(self, id):
        cliente = self.buscar_cliente_por_id(id)
        if cliente:
            self.clientes.remove(cliente)
            return True
        return False