from flask import request
from flask_restx import Resource
from flask_restx import Namespace
from modules.backoffice.user.infrastructure.controllers.flask_restx import AllUsersController
from modules.backoffice.user.infrastructure.controllers.flask_restx import UserFinderController
from modules.backoffice.user.infrastructure.controllers.flask_restx import UserCreatorController
from modules.backoffice.user.infrastructure.controllers.flask_restx import UserDeleterController

namespace = Namespace(name="user", description="Users")


@namespace.route("/")
class ListUser(Resource):
    def get(self):
        all_users_controller = AllUsersController()
        response = all_users_controller()
        return response

    def post(self):
        data = request.json
        user_creator_controller = UserCreatorController()
        response = user_creator_controller(body=data)
        return response


@namespace.route("/<string:user_id>")
class User(Resource):
    def get(self, user_id):
        user_finder_controller = UserFinderController()
        response = user_finder_controller(user_id=user_id)
        return response

    def delete(self, user_id):
        user_deleter_controller = UserDeleterController()
        response = user_deleter_controller(user_id=user_id)
        return response
