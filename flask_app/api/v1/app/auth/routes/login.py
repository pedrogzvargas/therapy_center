from flask import request
from flask_restx import Resource
from flask_restx import Namespace
from modules.app.auth.infrastructure.controllers.flask_restx import LoginController

namespace = Namespace(name="login", description="Login for users")


@namespace.route("/")
class Login(Resource):
    def post(self):
        data = request.json
        login_controller = LoginController()
        token = login_controller(body=data)
        return token
