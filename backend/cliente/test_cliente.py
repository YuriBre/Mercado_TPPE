import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

cliente_exemplo = {
    "cpf": "12345678900",
    "nome": "João Silva",
    "endereco": "Rua A, Bairro B",
    "telefone": "11999999999"
}

@pytest.fixture
def novo_cliente():
    response = client.post("/clientes/clientes", json=cliente_exemplo)
    assert response.status_code == 200
    yield response
    client.delete(f"/clientes/clientes/{cliente_exemplo['cpf']}")

def test_adicionar_cliente():
    response = client.post("/clientes/clientes", json=cliente_exemplo)
    assert response.status_code == 200
    assert response.json()["cpf"] == cliente_exemplo["cpf"]
    assert response.json()["nome"] == cliente_exemplo["nome"]
    assert response.json()["endereco"] == cliente_exemplo["endereco"]
    assert response.json()["telefone"] == cliente_exemplo["telefone"]
    client.delete(f"/clientes/clientes/{cliente_exemplo['cpf']}")

@pytest.mark.usefixtures("novo_cliente")
def test_listar_clientes():
    response = client.get("/clientes/clientes")
    assert response.status_code == 200
    assert any(cliente["cpf"] == cliente_exemplo["cpf"] for cliente in response.json())

@pytest.mark.usefixtures("novo_cliente")
def test_buscar_cliente():
    response = client.get(f"/clientes/clientes/{cliente_exemplo['cpf']}")
    assert response.status_code == 200
    assert response.json()["cpf"] == cliente_exemplo["cpf"]

@pytest.mark.usefixtures("novo_cliente")
def test_atualizar_cliente():
    novo_dado = {
    "cpf": cliente_exemplo["cpf"],
    "nome": "João Atualizado",
    "endereco": "Rua C, Bairro D",
    "telefone": "11888888888"
    }
    response = client.put(f"/clientes/clientes/{cliente_exemplo['cpf']}", json=novo_dado)
    assert response.status_code == 200
    assert response.json()["telefone"] == novo_dado["telefone"]

def test_remover_cliente():
    client.post("/clientes/clientes", json=cliente_exemplo)
    response = client.delete(f"/clientes/clientes/{cliente_exemplo['cpf']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente removcpfo com sucesso!"
