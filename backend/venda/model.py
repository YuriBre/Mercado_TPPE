from sqlalchemy import Column, Integer, Float, ForeignKey
from database import Base

class ModeloVenda(Base):
    __tablename__ = "venda"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False, default=0.00)