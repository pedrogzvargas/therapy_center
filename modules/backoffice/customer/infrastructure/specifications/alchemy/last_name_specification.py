from modules.shared.speficication.domain import Specification
from sqlalchemy_models.customer_model import BackofficeCustomer


class LastNameSpecification(Specification):

    def __init__(self, last_name):
        self.last_name = last_name

    def is_satisfied_by(self, entity):
        return self.last_name.lower() in entity.last_name.lower()

    def apply(self, query):
        return query.filter(BackofficeCustomer.last_name.ilike(f"%{self.last_name}%"))
