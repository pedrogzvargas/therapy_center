from uuid import UUID

from modules.app.payment_method.domain import PaymentMethodRepository
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.persistence.infraestructure import AlchemySessionCreator
from sqlalchemy_models.payment_method_model import AppPaymentMethod as PaymentMethod


class PostgresPaymentMethodRepository(PaymentMethodRepository):
    """
    PostgresPaymentMethodRepository
    """

    def __init__(self, environ: Environ = None):
        self.__environ = environ or PyEnviron()
        self.__session = AlchemySessionCreator(
            dialect=self.__environ.get_str("POSTGRES_DIALECT"),
            driver=self.__environ.get_str("POSTGRES_DRIVER"),
            host=self.__environ.get_str("POSTGRES_HOST"),
            user=self.__environ.get_str("POSTGRES_USER"),
            password=self.__environ.get_str("POSTGRES_PASSWORD"),
            port=self.__environ.get_str("POSTGRES_PORT"),
            db=self.__environ.get_str("POSTGRES_DB"),
        ).get_session()

    def all(self):
        """list all payment methods"""
        with self.__session as session:
            result = session.query(PaymentMethod).all()
        return result

    def get(self, id: UUID):
        """get payment method"""
        with self.__session as session:
            payment_method = session.get(PaymentMethod, id)
        return payment_method
