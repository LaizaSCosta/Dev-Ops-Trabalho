from app import app


def test_inicio():
    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert resposta.json["status"] == "online"


def test_criar_tarefa():
    cliente = app.test_client()

    resposta = cliente.post(
        "/tarefas",
        json={"titulo": "Estudar Docker"}
    )

    assert resposta.status_code == 201
    assert resposta.json["titulo"] == "Estudar Docker"
    assert resposta.json["concluida"] is False