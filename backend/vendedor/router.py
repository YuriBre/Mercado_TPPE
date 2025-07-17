from vendedor.schemas import VendedorCreate, VendedorBase
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from vendedor.model import ModeloVendedor
from database import get_db

router = APIRouter()

@router.get("/vendedores", response_model=list[VendedorBase])
def listar_vendedores(db: Session = Depends(get_db)):
    return db.query(ModeloVendedor).all()

@router.post("/vendedores", response_model=VendedorBase)
def adicionar_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    novo_vendedor = ModeloVendedor(**vendedor.dict())
    db.add(novo_vendedor)
    db.commit()
    db.refresh(novo_vendedor)
    return novo_vendedor

@router.get("/vendedores/{cpf}", response_model=VendedorBase)
def buscar_vendedor(cpf: str, db: Session = Depends(get_db)):
    vendedor = db.query(ModeloVendedor).filter(ModeloVendedor.cpf == cpf).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="vendedor não encontrado")
    return vendedor

@router.put("/vendedores/{cpf}", response_model=VendedorBase)
def atualizar_vendedor(cpf: str, vendedor_update: VendedorCreate, db: Session = Depends(get_db)):
    vendedor = db.query(ModeloVendedor).filter(ModeloVendedor.cpf == cpf).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="vendedor não encontrado")
    
    for chave, valor in vendedor_update.dict(exclude_unset=True).items():
        setattr(vendedor, chave, valor)
    
    db.commit()
    db.refresh(vendedor)
    return vendedor

@router.delete("/vendedores/{cpf}")
def remover_vendedor(cpf: str, db: Session = Depends(get_db)):
    vendedor = db.query(ModeloVendedor).filter(ModeloVendedor.cpf == cpf).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="vendedor não encontrado")
    db.delete(vendedor)
    db.commit()
    return {"message": "vendedor removcpfo com sucesso!"}