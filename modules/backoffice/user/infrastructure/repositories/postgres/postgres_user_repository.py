from uuid import UUID
from sqlalchemy.orm import Session

from modules.backoffice.user.domain import UserRepository
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.persistence.infraestructure import AlchemySessionCreator
from modules.backoffice.user.domain import User


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

    def add(self, user):
        """add user to session"""
        self.__session.add(user)
        self.__session.flush()

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

    def save(self, user):
        """save user"""
        with self.__session as session:
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                session.rollback()

    def delete(self, user):
        """delete user"""
        with self.__session as session:
            session.delete(user)
            session.commit()

    def soft_delete(self, user):
        """soft delete user"""

        if not hasattr(user, "is_active"):
            raise ValueError("User model has not 'is_active' attribute")

        user.is_active = False

        with self.__session as session:
            session.delete(user)
            session.commit()
