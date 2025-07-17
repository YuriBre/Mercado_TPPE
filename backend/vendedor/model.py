from sqlalchemy import Column, String
from database import Base

class ModeloVendedor(Base):
    __tablename__ = "vendedor"

    cpf = Column(String(14), primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
