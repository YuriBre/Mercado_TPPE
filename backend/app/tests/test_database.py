import pytest
from app.db.database import database

@pytest.mark.asyncio
async def test_database_connection():
    try:
        await database.connect()
        assert database.is_connected
    finally:
        await database.disconnect()

@pytest.mark.asyncio
async def test_insert_and_delete():
    try:
        await database.connect()

        # Insere um produto no banco de dados
        query = "INSERT INTO produtos (nome, preco, quantidade) VALUES (:nome, :preco, :quantidade)"
        values = {"nome": "Produto Teste", "preco": 100, "quantidade": 10}
        await database.execute(query, values)

        # Verifica se o produto foi inserido
        select_query = "SELECT * FROM produtos WHERE nome = :nome"
        result = await database.fetch_one(select_query, {"nome": "Produto Teste"})
        assert result is not None

        # Deleta o produto inserido
        delete_query = "DELETE FROM produtos WHERE nome = :nome"
        await database.execute(delete_query, {"nome": "Produto Teste"})

        # Verifica se o produto foi deletado
        result = await database.fetch_one(select_query, {"nome": "Produto Teste"})
        assert result is None
    finally:
        await database.disconnect()