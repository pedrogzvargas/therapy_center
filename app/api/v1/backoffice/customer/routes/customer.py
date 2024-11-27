from flask import request
from flask_restx import Resource
from flask_restx import Namespace
from modules.backoffice.customer.infrastructure.controllers.flask_restx import SearchCustomersController
from modules.backoffice.customer.infrastructure.controllers.flask_restx import CustomerFinderController
from modules.backoffice.customer.infrastructure.controllers.flask_restx import CustomerCreatorController
from modules.backoffice.customer.infrastructure.controllers.flask_restx import CustomerDeleterController

from app.api.v1.backoffice.customer.parsers import ParseArgs

namespace = Namespace(name="customer", description="Customers")


@namespace.route("/")
class ListCustomer(Resource):
    def get(self):
        args = ParseArgs.build().parse_args()
        search_customers_controller = SearchCustomersController()
        response = search_customers_controller(
            query_params=args,
            page_size=int(args.get("page_size", 10)),
            page=int(args.get("page", 1)),
        )
        return response

    def post(self):
        data = request.json
        customer_creator_controller = CustomerCreatorController()
        response = customer_creator_controller(body=data)
        return response


@namespace.route("/<string:customer_id>")
class Customer(Resource):
    def get(self, customer_id):
        customer_finder_controller = CustomerFinderController()
        response = customer_finder_controller(customer_id=customer_id)
        return response

    def delete(self, customer_id):
        customer_deleter_controller = CustomerDeleterController()
        response = customer_deleter_controller(customer_id=customer_id)
        return response
