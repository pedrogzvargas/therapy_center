from flask import Flask
from app.api.v1.app.blueprint_v1 import blueprint as app_blueprint
from app.api.v1.backoffice.blueprint_v1 import blueprint as backoffice_blueprint


def create_app(test_config=None):
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(app_blueprint)
    app.register_blueprint(backoffice_blueprint)
