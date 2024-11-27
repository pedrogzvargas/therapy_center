from uuid import UUID
from sqlalchemy.orm import Session

from modules.app.user.domain import UserRepository
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.persistence.infraestructure import AlchemySessionCreator
from modules.app.user.domain import User


class PostgresUserRepository(UserRepository):
    """
    PostgresUserRepository
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
        """list all users"""
        with self.__session as session:
            result = session.query(User).all()
        return result

    def get(self, id: UUID):
        """get user"""
        with self.__session as session:
            user = session.get(User, id)
        return user

    def get_by_username(self, username: str):
        """get user"""
        with self.__session as session:
            user = session.query(User).filter_by(username=username).first()
        return user

    def save(self, user):
        """save user"""
        with self.__session as session:
            session.add(user)
            session.commit()

    def delete(self, user):
        """delete user"""
        with self.__session as session:
            session.delete(user)
            session.commit()
