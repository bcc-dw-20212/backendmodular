from flask import Blueprint, jsonify, request

from backendmodular.ext.database import db
from sqlalchemy import exc

from backendmodular.models import Receitas


bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@bp.get("/")
def root():
    return jsonify(Receitas.query.all()), 200


@bp.post("/")
def insert_receita():
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
