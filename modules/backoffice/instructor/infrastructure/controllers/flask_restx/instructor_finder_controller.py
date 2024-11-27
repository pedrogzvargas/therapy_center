from uuid import UUID
from modules.backoffice.instructor.domain import InstructorRepository
from modules.backoffice.instructor.domain import InstructorDoesNotExist
from modules.backoffice.instructor.application.find import InstructorFinder
from modules.backoffice.instructor.infrastructure.repositories.postgres import PostgresInstructorRepository
from modules.backoffice.instructor.infrastructure.schemas.marshmallow import InstructorSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class InstructorFinderController:
    """
    Class controller to get Instructor
    """

    def __init__(
        self,
        instructor_repository: InstructorRepository = None,
        entity_serializer: EntitySerializer = None,
        environ: Environ = None
    ):
        """
        Args:
            instructor_repository: repository for instructor database table operations
            entity_serializer: serializer class
            environ: environ variable reader
        """

        self.__environ = environ or PyEnviron()
        self.__instructor_repository = instructor_repository or PostgresInstructorRepository(environ=self.__environ)
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=InstructorSchema())

    def __call__(self, instructor_id: UUID):
        try:
            instructor_finder = InstructorFinder(instructor_repository=self.__instructor_repository)
            instructor = instructor_finder(instructor_id=instructor_id)
            instructor = self.__entity_serializer(instructor)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": instructor
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
