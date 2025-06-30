from sqlalchemy import Column, Integer, String
from database import Base

class ModeloCliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(150), nullable=False)
    telefone = Column(String(20), nullable=False)
