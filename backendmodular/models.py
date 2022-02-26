from typing import Dict
from backendmodular.ext.database import db


class Receitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(30), unique=True, nullable=False)
    descricao = db.Column(db.String(500), nullable=False)

    def to_json(self) -> Dict:
        return {"id": self.id, "titulo": self.titulo, "descricao": self.descricao}

    def __str__(self) -> str:
        return str(self.to_json())
