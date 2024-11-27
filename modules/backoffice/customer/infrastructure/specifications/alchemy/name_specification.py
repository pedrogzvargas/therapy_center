from modules.shared.speficication.domain import Specification
from sqlalchemy_models.customer_model import BackofficeCustomer


class NameSpecification(Specification):

    def __init__(self, name):
        self.name = name

    def is_satisfied_by(self, entity):
        return self.name.lower() in entity.name.lower()

    def apply(self, query):
        return query.filter(BackofficeCustomer.name.ilike(f"%{self.name}%"))
