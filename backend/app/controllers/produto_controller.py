from fastapi import APIRouter
from app.db.database import database

router = APIRouter()

@router.post("/")
async def inserir_produto(nome: str, preco: int, quantidade: int):
    query = "INSERT INTO produtos (nome, preco, quantidade) VALUES (:nome, :preco, :quantidade)"
    await database.execute(query, values={"nome": nome, "preco": preco, "quantidade": quantidade})
    return {"message": "Produto inserido com sucesso!"}

@router.get("/")
async def listar_produtos():
    query = "SELECT * FROM produtos"
    produtos = await database.fetch_all(query)
    return {"produtos": produtos}

@router.delete("/{produto_id}")
async def deletar_produto(produto_id: int):
    query = "DELETE FROM produtos WHERE id = :produto_id"
    await database.execute(query, values={"produto_id": produto_id})
    return {"message": "Produto deletado com sucesso!"}