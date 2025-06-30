from database import Base
from sqlalchemy import Column, Integer, String, Float

class ModeloProduto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    lucro_percentual = Column(Float, nullable=False)
    qtd_estoque = Column(Integer, nullable=False)
