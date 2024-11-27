from flask import Blueprint
from flask_restx import Api

from app.api.v1.backoffice.payment_method.routes.payment_method import namespace as payment_method_ns
from app.api.v1.backoffice.user.routes.user import namespace as user_ns
from app.api.v1.backoffice.service.routes.service import namespace as service_ns
from app.api.v1.backoffice.instructor.routes.instructor import namespace as instructor_ns
from app.api.v1.backoffice.customer.routes.customer import namespace as customer_ns

blueprint = Blueprint("api_backoffice", __name__, url_prefix="/backoffice/api/v1")
api = Api(blueprint)

api.add_namespace(payment_method_ns, "/payment-method")
api.add_namespace(service_ns, "/service")
api.add_namespace(user_ns, "/user")
api.add_namespace(instructor_ns, "/instructor")
api.add_namespace(customer_ns, "/customer")
