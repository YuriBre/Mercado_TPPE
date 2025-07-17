from pydantic import BaseModel

class VendedorBase(BaseModel):
    cpf: str
    nome: str
    email: str
    telefone: str

class VendedorCreate(VendedorBase):
    pass

class Vendedor(VendedorBase):
    cpf: str

    class Config:
        orm_mode = True

class VendedorResponse(BaseModel):
    cpf: str
    nome: str

    class Config:
        orm_mode = True