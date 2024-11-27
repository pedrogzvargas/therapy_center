from uuid import UUID
from modules.backoffice.instructor.domain import InstructorRepository
from modules.backoffice.instructor.domain import InstructorDoesNotExist
from modules.backoffice.instructor.application.delete import InstructorDeleter
from modules.backoffice.instructor.infrastructure.repositories.postgres import PostgresInstructorRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron


class InstructorDeleterController:
    """
    Class controller to delete Instructor
    """

    def __init__(
        self,
        instructor_repository: InstructorRepository = None,
        environ: Environ = None
    ):
        """
        Args:
            instructor_repository: repository for instructor database table operations
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__instructor_repository = instructor_repository or PostgresInstructorRepository(environ=self.__environ)

    def __call__(self, instructor_id: UUID):
        try:
            instructor_deleter = InstructorDeleter(instructor_repository=self.__instructor_repository)
            instructor_deleter(instructor_id=instructor_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except InstructorDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
