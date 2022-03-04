from flask import Blueprint, jsonify, request

from backendmodular.ext.database import db
from sqlalchemy import exc

from backendmodular.models import Receitas


bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@bp.get("/")
def root():
    """
    Lista todas as receitas.
    ---
    description: Retorna uma lista de receitas.
    produces: application/json
    tags:
      - receitas
    responses:
      200:
        description: Lista de Usuários
    """
    return jsonify(Receitas.query.all()), 200


@bp.post("/")
def insert_receita():
    """
    Insere nova receita.
    ---
    description: Faz isso e aquilo.
    produces: application/json
    tags:
      - receitas
    responses:
      201:
        description: Receita inserida com sucesso.
      406:
        description: Erro de integridade.
    """
    json = request.get_json()

    nova = Receitas()
    nova.titulo = json["titulo"]
    nova.descricao = json["descricao"]
    try:
        db.session.add(nova)
        db.session.commit()

        confirm = Receitas.query.get(nova.id)

        return jsonify(confirm.to_json()), 201
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "integrity error"}), 406


@bp.get("/<int:id>")
def get_single_receita(id):
    item = Receitas.query.get(id)

    if item:
        return jsonify(item.to_json()), 200
    else:
        return jsonify({"message": "item not found"}), 404


@bp.put("/")
def uptade_receita():
    item = Receitas.query.get(request.get_json()["id"])

    if item:
        item.titulo = request.get_json()["titulo"]
        item.descricao = request.get_json()["descricao"]

        try:
            db.session.add(item)
            db.session.commit()

            confirm = Receitas.query.get(request.get_json()["id"])

            return jsonify(confirm.to_json()), 201
        except exc.IntegrityError:
            db.session.rollback()
            return jsonify({"message": "integrity error"}), 406
    else:
        return jsonify({"message": "item not found"}), 403


@bp.delete("/")
def removes_receita():
    id = request.get_json()["id"]

    item = Receitas.query.get(id)

    if item:
        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "item removed"}), 201
    else:
        return jsonify({"message": "item not found"}), 404


def init_app(app):
    app.register_blueprint(bp)
