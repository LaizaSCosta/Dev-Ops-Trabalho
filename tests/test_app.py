import pytest

from app import app, tarefas


@pytest.fixture(autouse=True)
def limpar_tarefas():
    tarefas.clear()
    yield
    tarefas.clear()


def test_inicio():
    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert resposta.json["status"] == "online"
    assert resposta.json["mensagem"] == "API de Lista de Tarefas"


def test_listar_tarefas_vazia():
    cliente = app.test_client()

    resposta = cliente.get("/tarefas")

    assert resposta.status_code == 200
    assert resposta.json == []


def test_criar_tarefa():
    cliente = app.test_client()

    resposta = cliente.post(
        "/tarefas",
        json={"titulo": "Estudar Docker"}
    )

    assert resposta.status_code == 201
    assert resposta.json["id"] == 1
    assert resposta.json["titulo"] == "Estudar Docker"
    assert resposta.json["concluida"] is False


def test_criar_tarefa_sem_titulo():
    cliente = app.test_client()

    resposta = cliente.post(
        "/tarefas",
        json={}
    )

    assert resposta.status_code == 400
    assert resposta.json["erro"] == "O título da tarefa é obrigatório"


def test_concluir_tarefa():
    cliente = app.test_client()

    cliente.post(
        "/tarefas",
        json={"titulo": "Estudar Python"}
    )

    resposta = cliente.put("/tarefas/1")

    assert resposta.status_code == 200
    assert resposta.json["id"] == 1
    assert resposta.json["concluida"] is True


def test_concluir_tarefa_inexistente():
    cliente = app.test_client()

    resposta = cliente.put("/tarefas/999")

    assert resposta.status_code == 404
    assert resposta.json["erro"] == "Tarefa não encontrada"


def test_excluir_tarefa():
    cliente = app.test_client()

    cliente.post(
        "/tarefas",
        json={"titulo": "Estudar GitHub Actions"}
    )

    resposta = cliente.delete("/tarefas/1")

    assert resposta.status_code == 200
    assert resposta.json["mensagem"] == "Tarefa excluída com sucesso"

    resposta_lista = cliente.get("/tarefas")

    assert resposta_lista.json == []