from flask import Flask, jsonify, request

app = Flask(__name__)

tarefas = []


@app.route("/")
def inicio():
    return jsonify({
        "mensagem": "API de Lista de Tarefas",
        "status": "online"
    })


@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    dados = request.get_json()

    if not dados or "titulo" not in dados:
        return jsonify({"erro": "O título da tarefa é obrigatório"}), 400

    tarefa = {
        "id": len(tarefas) + 1,
        "titulo": dados["titulo"],
        "concluida": False
    }

    tarefas.append(tarefa)

    return jsonify(tarefa), 201


@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
def concluir_tarefa(tarefa_id):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa["concluida"] = True
            return jsonify(tarefa)

    return jsonify({"erro": "Tarefa não encontrada"}), 404


@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
def excluir_tarefa(tarefa_id):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefas.remove(tarefa)
            return jsonify({"mensagem": "Tarefa excluída com sucesso"})

    return jsonify({"erro": "Tarefa não encontrada"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)