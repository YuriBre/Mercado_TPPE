from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    cpf: str
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None

    class Config:
        orm_mode = True

class ClienteCreate(ClienteBase):
    endereco: Optional[str] = None
    telefone: Optional[str] = None

class ClienteResponse(ClienteBase):
    pass