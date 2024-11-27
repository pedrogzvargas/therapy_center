from uuid import UUID
from modules.backoffice.instructor.domain import InstructorRepository
from modules.backoffice.instructor.domain import InstructorFinder as DomainInstructorFinder


class InstructorDeleter:
    """
    Class to delete Instructor
    """

    def __init__(self, instructor_repository: InstructorRepository):
        """
        Args:
            instructor_repository: repository for instructor database table operations
        """
        self.__instructor_repository = instructor_repository

    def __call__(self, instructor_id: UUID):
        instructor_finder = DomainInstructorFinder(instructor_repository=self.__instructor_repository)
        instructor = instructor_finder(instructor_id=instructor_id)
        self.__instructor_repository.delete(instructor)
