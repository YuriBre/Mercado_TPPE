from produto.schemas import ProdutoCreate, ProdutoBase
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from produto.model import ModeloProduto
from database import get_db

router = APIRouter()

@router.get("/produtos", response_model=list[ProdutoBase])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ModeloProduto).all()

@router.post("/produtos", response_model=ProdutoBase)
def adicionar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ModeloProduto(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/produtos/{produto_id}", response_model=ProdutoBase)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ModeloProduto).filter(ModeloProduto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.put("/produtos/{produto_id}", response_model=ProdutoBase)
def atualizar_produto(produto_id: int, produto_update: ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(ModeloProduto).filter(ModeloProduto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    for chave, valor in produto_update.dict(exclude_unset=True).items():
        setattr(produto, chave, valor)
    
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/produtos/{produto_id}")
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ModeloProduto).filter(ModeloProduto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"message": "Produto removido com sucesso!"}