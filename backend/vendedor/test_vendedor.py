import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

vendedor_exemplo = {
    "cpf": "12345678900",
    "nome": "João Silva",
    "email": "vendedor@email.com",
    "telefone": "11999999999"
}

@pytest.fixture
def novo_vendedor():
    response = client.post("/vendedores/vendedores", json=vendedor_exemplo)
    assert response.status_code == 200
    yield response
    client.delete(f"/vendedores/vendedores/{vendedor_exemplo['cpf']}")

def test_adicionar_vendedor():
    response = client.post("/vendedores/vendedores", json=vendedor_exemplo)
    assert response.status_code == 200
    assert response.json()["cpf"] == vendedor_exemplo["cpf"]
    assert response.json()["nome"] == vendedor_exemplo["nome"]
    assert response.json()["email"] == vendedor_exemplo["email"]
    assert response.json()["telefone"] == vendedor_exemplo["telefone"]
    client.delete(f"/vendedores/vendedores/{vendedor_exemplo['cpf']}")

@pytest.mark.usefixtures("novo_vendedor")
def test_listar_vendedores():
    response = client.get("/vendedores/vendedores")
    assert response.status_code == 200
    assert any(vendedor["cpf"] == vendedor_exemplo["cpf"] for vendedor in response.json())

@pytest.mark.usefixtures("novo_vendedor")
def test_buscar_vendedor():
    response = client.get(f"/vendedores/vendedores/{vendedor_exemplo['cpf']}")
    assert response.status_code == 200
    assert response.json()["cpf"] == vendedor_exemplo["cpf"]

@pytest.mark.usefixtures("novo_vendedor")
def test_atualizar_vendedor():
    novo_dado = {
    "cpf": vendedor_exemplo["cpf"],
    "nome": "João Atualizado",
    "email": "vendedor10@email.com",
    "telefone": "11888888888"
    }
    response = client.put(f"/vendedores/vendedores/{vendedor_exemplo['cpf']}", json=novo_dado)
    assert response.status_code == 200
    assert response.json()["telefone"] == novo_dado["telefone"]

def test_remover_vendedor():
    client.post("/vendedores/vendedores", json=vendedor_exemplo)
    response = client.delete(f"/vendedores/vendedores/{vendedor_exemplo['cpf']}")
    assert response.status_code == 200
    assert response.json()["message"] == "vendedor removcpfo com sucesso!"
