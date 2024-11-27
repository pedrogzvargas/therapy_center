from uuid import UUID
from sqlalchemy.orm import Session

from modules.backoffice.instructor.domain import InstructorRepository
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.persistence.infraestructure import AlchemySessionCreator
from modules.backoffice.instructor.domain import Instructor


class PostgresInstructorRepository(InstructorRepository):
    """
    PostgresInstructorRepository
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

    def add(self, instructor):
        """add instructor to session"""
        self.__session.add(instructor)
        self.__session.flush()

    def all(self):
        """list all instructors"""
        with self.__session as session:
            result = session.query(Instructor).all()
        return result

    def get(self, id: UUID):
        """get instructor"""
        with self.__session as session:
            instructor = session.get(Instructor, id)
        return instructor

    def save(self, instructor):
        """save instructor"""
        with self.__session as session:
            try:
                session.add(instructor)
                session.commit()
            except Exception as e:
                session.rollback()

    def delete(self, instructor):
        """delete instructor"""
        with self.__session as session:
            session.delete(instructor)
            session.commit()
