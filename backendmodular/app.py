from flask import Flask
from backendmodular.ext import configuration
from .views import root


def create_app() -> Flask:
    app = Flask(__name__)
    configuration.init_app(app)

    app.add_url_rule('/', view_func=root)

    return app