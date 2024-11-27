from modules.backoffice.instructor.domain import InstructorRepository
from modules.backoffice.instructor.application.all import AllInstructors
from modules.backoffice.instructor.infrastructure.repositories.postgres import PostgresInstructorRepository
from modules.backoffice.instructor.infrastructure.schemas.marshmallow import InstructorSchema
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infraestructure import PyEnviron
from modules.shared.serializer.infraestructure.marshmallow import MarshmallowEntitySerializer


class AllInstructorsController:
    """
    Class controller to get all Instructors
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

    def __call__(self):
        try:
            all_instructors = AllInstructors(instructor_repository=self.__instructor_repository)
            all_instructors = all_instructors()
            instructors = self.__entity_serializer(all_instructors, many=True)
            response = {"success": True, "message": "OK", "data": instructors}, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
