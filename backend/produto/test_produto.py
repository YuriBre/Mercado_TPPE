import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def gerar_produto():
    return {
        "nome": "Produto Teste",
        "descricao": "Descrição do produto teste",
        "valor": 19.99,
        "lucro_percentual": 20.0,
        "qtd_estoque": 50
    }

@pytest.fixture
def novo_produto():
    produto = gerar_produto()
    response = client.post("/produtos/produtos", json=produto)
    assert response.status_code == 200
    produto_criado = response.json()
    yield produto_criado
    client.delete(f"/produtos/produtos/{produto_criado['id']}")

def test_adicionar_produto():
    produto = gerar_produto()
    response = client.post("/produtos/produtos", json=produto)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == produto["nome"]
    assert data["descricao"] == produto["descricao"]
    assert data["valor"] == produto["valor"]
    assert data["lucro_percentual"] == produto["lucro_percentual"]
    assert data["qtd_estoque"] == produto["qtd_estoque"]
    client.delete(f"/produtos/produtos/{data['id']}")

@pytest.mark.usefixtures("novo_produto")
def test_listar_produtos(novo_produto):
    response = client.get("/produtos/produtos")
    assert response.status_code == 200
    assert any(produto["id"] == novo_produto["id"] for produto in response.json())

@pytest.mark.usefixtures("novo_produto")
def test_buscar_produto(novo_produto):
    response = client.get(f"/produtos/produtos/{novo_produto['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == novo_produto["id"]

@pytest.mark.usefixtures("novo_produto")
def test_atualizar_produto(novo_produto):
    novo_dado = {
        "nome": "Produto Atualizado",
        "descricao": "Nova descrição",
        "valor": 29.99,
        "lucro_percentual": 30.0,
        "qtd_estoque": 80
    }
    response = client.put(f"/produtos/produtos/{novo_produto['id']}", json=novo_dado)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == novo_dado["nome"]
    assert data["descricao"] == novo_dado["descricao"]
    assert data["valor"] == novo_dado["valor"]
    assert data["lucro_percentual"] == novo_dado["lucro_percentual"]
    assert data["qtd_estoque"] == novo_dado["qtd_estoque"]

def test_remover_produto():
    produto = gerar_produto()
    response = client.post("/produtos/produtos", json=produto)
    produto_id = response.json()["id"]
    response = client.delete(f"/produtos/produtos/{produto_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Produto removido com sucesso!"
