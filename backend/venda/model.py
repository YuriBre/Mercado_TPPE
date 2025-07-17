from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class ModeloVenda(Base):
    __tablename__ = "venda"

    id = Column(Integer, primary_key=True, index=True)
    cliente_cpf = Column(String, ForeignKey("cliente.cpf"), nullable=False)
    vendedor_cpf = Column(String, ForeignKey("vendedor.cpf"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    valor_total = Column(Float, nullable=False, default=0.00)

    cliente = relationship("ModeloCliente", backref="vendas")
    vendedor = relationship("ModeloVendedor", backref="vendas")
    produto = relationship("ModeloProduto", backref="vendas")