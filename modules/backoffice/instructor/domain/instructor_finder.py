from uuid import UUID
from .instructor_repository import InstructorRepository
from .instructor_does_not_exist import InstructorDoesNotExist


class InstructorFinder:
    """
    Class to get Instructor
    """

    def __init__(self, instructor_repository: InstructorRepository):
        """
        Args:
            instructor_repository: repository for instructor database table operations
        """
        self.__instructor_repository = instructor_repository

    def __call__(self, instructor_id: UUID):
        instructor = self.__instructor_repository.get(id=instructor_id)

        if not instructor:
            raise InstructorDoesNotExist(f"Instructor with id: {instructor_id} does not exist")

        return instructor
