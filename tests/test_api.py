from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensagem": "Bem-vindo à API de Recomendação de Produtos"
    }


produto1 = {"nome": "A", "categoria": "B", "tags": ["C", "D"]}
produto2 = {"nome": "Z", "categoria": "Y", "tags": ["W", "X"]}


def test_criar_produto():
    response = client.post("/produtos/", json=produto1)
    json = response.json()

    assert response.status_code == 200
    assert json["nome"] == produto1["nome"]
    assert json["categoria"] == produto1["categoria"]
    assert json["tags"][0] == produto1["tags"][0]
    assert json["tags"][1] == produto1["tags"][1]
    assert json["id"]

    client.post("/produtos/", json=produto2)


def test_listar_produtos():
    response = client.get("/produtos/")
    json = response.json()

    assert response.status_code == 200
    assert len(json) == 2
    assert json[0]["nome"] == produto1["nome"]
    assert json[0]["categoria"] == produto1["categoria"]
    assert json[0]["tags"][0] == produto1["tags"][0]
    assert json[0]["tags"][1] == produto1["tags"][1]


usuario1 = {"nome": "A"}
usuario2 = {"nome": "B"}


def test_criar_usuario():
    response = client.post("/usuarios/", params=usuario1)
    json = response.json()

    assert response.status_code == 200
    assert json["nome"] == usuario1["nome"]
    assert json["id"]

    client.post("/usuarios/", params=usuario2)


def test_listar_usuarios():
    response = client.get("/usuarios/")
    json = response.json()

    assert response.status_code == 200
    assert len(json) == 2
    assert json[0]["nome"] == usuario1["nome"]
    assert json[1]["nome"] == usuario2["nome"]


def test_criar_historico():
    historico = {"produtos_ids": [1, 2]}

    response = client.post("/historico_compras/1", json=historico)

    assert response.status_code == 200
    assert response.json() == {"mensagem": "Histórico de compras atualizado"}


def teste_recomendacoes_categoria():
    preferencias = {"categorias": [produto1["categoria"]], "tags": []}

    response = client.post("/recomendacoes/1", json=preferencias)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == produto1["nome"]


def teste_recomendacoes_tag():
    preferencias = {"categorias": [], "tags": [produto2["tags"][0]]}

    response = client.post("/recomendacoes/1", json=preferencias)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == produto2["nome"]


def teste_recomendacoes_categoria_tag():
    preferencias = {
        "categorias": [produto1["categoria"], produto2["categoria"]],
        "tags": [produto1["tags"][1]],
    }

    response = client.post("/recomendacoes/1", json=preferencias)

    assert response.status_code == 200
    assert len(response.json()) == 1  # apenas produto1
    assert response.json()[0]["nome"] == produto1["nome"]
