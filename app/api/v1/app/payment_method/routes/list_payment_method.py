from flask_restx import Resource
from flask_restx import Namespace
from modules.app.payment_method.infrastructure.controllers.flask_restx import AllPaymentMethodsController
from modules.app.payment_method.infrastructure.controllers.flask_restx import PaymentMethodFinderController
from app.decorators import token_required

namespace = Namespace(name="payment-method", description="Payment Methods Catalog")


@namespace.route("/")
class ListPaymentMethod(Resource):
    @token_required
    def get(self):
        all_payment_methods_controller = AllPaymentMethodsController()
        all_payment_methods = all_payment_methods_controller()
        return all_payment_methods


@namespace.route("/<string:payment_method_id>")
class GetPaymentMethod(Resource):
    @token_required
    def get(self, payment_method_id):
        payment_method_finder_controller = PaymentMethodFinderController()
        payment_method = payment_method_finder_controller(payment_method_id=payment_method_id)
        return payment_method
