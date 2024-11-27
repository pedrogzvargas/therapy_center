from flask import request
from flask_restx import Resource
from flask_restx import Namespace
from modules.backoffice.service.infrastructure.controllers.flask_restx import AllServicesController
from modules.backoffice.service.infrastructure.controllers.flask_restx import ServiceFinderController
from modules.backoffice.service.infrastructure.controllers.flask_restx import ServiceCreatorController
from modules.backoffice.service.infrastructure.controllers.flask_restx import ServicePatcherController
from modules.backoffice.service.infrastructure.controllers.flask_restx import ServiceDeleterController

namespace = Namespace(name="service", description="Services Catalog")


@namespace.route("/")
class ListService(Resource):
    def get(self):
        all_services_controller = AllServicesController()
        response = all_services_controller()
        return response

    def post(self):
        data = request.json
        service_creator_controller = ServiceCreatorController()
        response = service_creator_controller(body=data)
        return response


@namespace.route("/<string:service_id>")
class Service(Resource):
    def get(self, service_id):
        service_finder_controller = ServiceFinderController()
        response = service_finder_controller(service_id=service_id)
        return response

    def patch(self, service_id):
        data = request.json
        service_patcher_controller = ServicePatcherController()
        response = service_patcher_controller(service_id=service_id, data=data)
        return response

    def delete(self, service_id):
        service_deleter_controller = ServiceDeleterController()
        response = service_deleter_controller(service_id=service_id)
        return response
