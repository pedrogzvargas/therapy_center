from uuid import UUID
from sqlalchemy.orm import Session

from modules.backoffice.customer.domain import CustomerRepository
from modules.backoffice.customer.domain import Customer
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.persistence.infraestructure import AlchemySessionCreator

from modules.shared.speficication.domain import Specification


class PostgresCustomerRepository(CustomerRepository):
    """
    PostgresCustomerRepository
    """

    def __init__(self, environ: Environ = None, session: Session = None):
        self.__environ = environ or PyEnviron()
        self.__session = session or AlchemySessionCreator(
            dialect=self.__environ.get_str("POSTGRES_DIALECT"),
            driver=self.__environ.get_str("POSTGRES_DRIVER"),
            host=self.__environ.get_str("POSTGRES_HOST"),
            user=self.__environ.get_str("POSTGRES_USER"),
            password=self.__environ.get_str("POSTGRES_PASSWORD"),
            port=self.__environ.get_str("POSTGRES_PORT"),
            db=self.__environ.get_str("POSTGRES_DB"),
        ).get_session()

    def add(self, customer):
        """add customer to session"""
        self.__session.add(customer)
        self.__session.flush()

    def search(self, specifications: list, page: int = 1, page_size: int = 10):
        """search customers"""
        with self.__session as session:
            query = session.query(Customer)
            for specification in specifications:
                query = specification.apply(query)
            total_results = query.count()
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)

            return {
                "results": query.all(),
                "page": page,
                "page_size": page_size,
                "total_results": total_results,
                "total_pages": (total_results + page_size - 1) // page_size,
            }

    def all(self):
        """list all customers"""
        with self.__session as session:
            result = session.query(Customer).all()
        return result

    def get(self, id: UUID):
        """get customer"""
        with self.__session as session:
            customer = session.get(Customer, id)
        return customer

    def save(self, customer):
        """save customer"""
        with self.__session as session:
            try:
                session.add(customer)
                session.commit()
            except Exception as e:
                session.rollback()

    def delete(self, customer):
        """delete customer"""
        with self.__session as session:
            session.delete(customer)
            session.commit()
