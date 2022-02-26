import pytest
from backendmodular.app import create_app
from backendmodular.ext.database import db


@pytest.fixture()
def client():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    with app.app_context():
        db.init_app(app)
        db.create_all()
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    with app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()


@pytest.fixture()
def item():
    return {
        "titulo": "Arroz carreteiro",
        "descricao": "Um arroz típico do sudeste do Brasil",
    }
