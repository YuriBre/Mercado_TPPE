from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db.database import database
from app.models import Produto, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

class ProdutoCreate(BaseModel):
    nome: str
    preco: int
    quantidade: int

@app.post("/produto/")
async def criar_produto(produto: ProdutoCreate):
    db = SessionLocal()
    produto_db = Produto(nome=produto.nome, preco=produto.preco, quantidade=produto.quantidade)
    db.add(produto_db)
    db.commit()
    db.refresh(produto_db)
    return produto_db
