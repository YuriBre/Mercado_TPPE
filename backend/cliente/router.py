from cliente.schemas import ClienteCreate, ClienteBase
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from cliente.model import ModeloCliente
from database import get_db

router = APIRouter()

@router.get("/clientes", response_model=list[ClienteBase])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(ModeloCliente).all()

@router.post("/clientes", response_model=ClienteBase)
def adicionar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = ModeloCliente(**cliente.dict())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@router.get("/clientes/{id}", response_model=ClienteBase)
def buscar_cliente(id: str, db: Session = Depends(get_db)):
    cliente = db.query(ModeloCliente).filter(ModeloCliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/clientes/{id}", response_model=ClienteBase)
def atualizar_cliente(id: str, cliente_update: ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(ModeloCliente).filter(ModeloCliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    for chave, valor in cliente_update.dict(exclude_unset=True).items():
        setattr(cliente, chave, valor)
    
    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/clientes/{id}")
def remover_cliente(id: str, db: Session = Depends(get_db)):
    cliente = db.query(ModeloCliente).filter(ModeloCliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente removido com sucesso!"}