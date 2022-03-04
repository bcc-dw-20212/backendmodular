from typing import NoReturn
from flask import Flask, jsonify
from flask_swagger import swagger


# Place here the extension's dependencies


# Place here your extension globals


def init_app(app: Flask) -> NoReturn:

    """Init your global objects which do need to connect to flask object."""

    def spec():
        return jsonify(swagger(app))

    app.add_url_rule("/spec", view_func=spec)
