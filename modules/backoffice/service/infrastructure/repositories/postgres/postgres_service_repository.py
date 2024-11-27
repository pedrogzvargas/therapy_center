from uuid import UUID
from sqlalchemy.orm import Session

from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.persistence.infraestructure import AlchemySessionCreator
from modules.backoffice.service.domain import ServiceRepository
from modules.backoffice.service.domain import Service


class PostgresServiceRepository(ServiceRepository):
    """
    PostgresServiceRepository
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

    def all(self):
        """list all services"""
        with self.__session as session:
            result = session.query(Service).all()
        return result

    def get(self, id: UUID):
        """get service"""
        with self.__session as session:
            service = session.get(Service, id)
        return service

    def save(self, service):
        """save service"""
        with self.__session as session:
            try:
                session.add(service)
                session.commit()
            except Exception as e:
                session.rollback()

    def delete(self, service):
        """delete service"""
        with self.__session as session:
            session.delete(service)
            session.commit()
