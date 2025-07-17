from sqlalchemy import Column, String
from database import Base

class ModeloCliente(Base):
    __tablename__ = "cliente"

    cpf = Column(String(14), primary_key=True, nullable=False)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(150), nullable=False)
    telefone = Column(String(20), nullable=False)
