from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensagem": "Bem-vindo à API de Recomendação de Produtos"
    }


produto = {"nome": "A", "categoria": "B", "tags": ["C", "D"]}


def test_criar_produto():
    response = client.post("/produtos/", json=produto)
    json = response.json()

    assert response.status_code == 200
    assert json["nome"] == produto["nome"]
    assert json["categoria"] == produto["categoria"]
    assert json["tags"][0] == produto["tags"][0]
    assert json["tags"][1] == produto["tags"][1]
    assert json["id"]


def test_listar_produtos():
    response = client.get("/produtos/")
    json = response.json()

    assert response.status_code == 200
    assert len(json) == 1
    assert json[0]["nome"] == produto["nome"]
    assert json[0]["categoria"] == produto["categoria"]
    assert json[0]["tags"][0] == produto["tags"][0]
    assert json[0]["tags"][1] == produto["tags"][1]


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


# def func(x):
#     return x + 1


# def test_answer():
#     assert func(3) == 5
