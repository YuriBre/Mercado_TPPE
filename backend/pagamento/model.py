import enum
from sqlalchemy import Column, Integer, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base

class MetodoPagamentoEnum(str, enum.Enum):
    dinheiro = "dinheiro"
    cartao = "cartao"
    pix = "pix"
    boleto = "boleto"

class ModeloPagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id", ondelete="CASCADE"), nullable=False)
    valor_pago = Column(DECIMAL(10, 2), nullable=False)
    metodo_pagamento = Column(Enum(MetodoPagamentoEnum), nullable=False)
    data_pagamento = Column(DateTime, server_default=func.now())
