from flask import request
from flask_restx import Resource
from flask_restx import Namespace
from modules.backoffice.payment_method.infrastructure.controllers.flask_restx import AllPaymentMethodsController
from modules.backoffice.payment_method.infrastructure.controllers.flask_restx import PaymentMethodFinderController
from modules.backoffice.payment_method.infrastructure.controllers.flask_restx import PaymentMethodCreatorController
from modules.backoffice.payment_method.infrastructure.controllers.flask_restx import PaymentMethodPatcherController
from modules.backoffice.payment_method.infrastructure.controllers.flask_restx import PaymentMethodDeleterController

namespace = Namespace(name="payment-method", description="Payment Methods Catalog")


@namespace.route("/")
class ListPaymentMethod(Resource):
    def get(self):
        all_payment_methods_controller = AllPaymentMethodsController()
        response = all_payment_methods_controller()
        return response

    def post(self):
        data = request.json
        payment_method_creator_controller = PaymentMethodCreatorController()
        response = payment_method_creator_controller(body=data)
        return response


@namespace.route("/<string:payment_method_id>")
class PaymentMethod(Resource):
    def get(self, payment_method_id):
        payment_method_finder_controller = PaymentMethodFinderController()
        response = payment_method_finder_controller(payment_method_id=payment_method_id)
        return response

    def patch(self, payment_method_id):
        data = request.json
        payment_method_patcher_controller = PaymentMethodPatcherController()
        response = payment_method_patcher_controller(payment_method_id=payment_method_id, data=data)
        return response

    def delete(self, payment_method_id):
        payment_method_deleter_controller = PaymentMethodDeleterController()
        response = payment_method_deleter_controller(payment_method_id=payment_method_id)
        return response
