from flask import Blueprint
from flask_restx import Api

from app.api.v1.app.payment_method.routes.list_payment_method import namespace as payment_method_ns
from app.api.v1.app.auth.routes.login import namespace as auth_ns

blueprint = Blueprint("api_app", __name__, url_prefix="/app/api/v1")
api = Api(blueprint)

api.add_namespace(payment_method_ns, "/payment-method")
api.add_namespace(auth_ns, "/login")
