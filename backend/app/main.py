import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database

DATABASE_URL = "mysql+aiomysql://user:user123@db:3306/mercado"
database = Database(DATABASE_URL)

app = FastAPI()

# Modelo para o produto
class Produto(BaseModel):
    nome: str
    preco: int
    quantidade: int

async def connect_with_retry():
    for attempt in range(10):
        try:
            await database.connect()
            print("Conectado ao banco!")
            return
        except Exception as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            await asyncio.sleep(3)
    raise Exception("Não foi possível conectar ao banco após várias tentativas")

@app.on_event("startup")
async def startup():
    await connect_with_retry()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "API funcionando!"}

# CRUD Simples

@app.post("/produtos/")
async def criar_produto(produto: Produto):
    query = "INSERT INTO produtos (nome, preco, quantidade) VALUES (:nome, :preco, :quantidade)"
    values = {"nome": produto.nome, "preco": produto.preco, "quantidade": produto.quantidade}
    await database.execute(query, values)
    return {"message": "Produto criado com sucesso!"}

@app.get("/produtos/")
async def listar_produtos():
    query = "SELECT * FROM produtos"
    produtos = await database.fetch_all(query)
    return {"produtos": produtos}

@app.get("/produtos/{produto_id}")
async def obter_produto(produto_id: int):
    query = "SELECT * FROM produtos WHERE id = :produto_id"
    produto = await database.fetch_one(query, {"produto_id": produto_id})
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/produtos/{produto_id}")
async def atualizar_produto(produto_id: int, produto: Produto):
    query = """
        UPDATE produtos
        SET nome = :nome, preco = :preco, quantidade = :quantidade
        WHERE id = :produto_id
    """
    values = {"nome": produto.nome, "preco": produto.preco, "quantidade": produto.quantidade, "produto_id": produto_id}
    result = await database.execute(query, values)
    if result == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto atualizado com sucesso!"}

@app.delete("/produtos/{produto_id}")
async def deletar_produto(produto_id: int):
    query = "DELETE FROM produtos WHERE id = :produto_id"
    result = await database.execute(query, {"produto_id": produto_id})
    if result == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso!"}