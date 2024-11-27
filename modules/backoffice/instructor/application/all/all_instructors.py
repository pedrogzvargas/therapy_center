from modules.backoffice.instructor.domain import InstructorRepository


class AllInstructors:
    """
    Class to get all Instructors
    """

    def __init__(self, instructor_repository: InstructorRepository):
        """
        Args:
            instructor_repository: repository for instructor database table operations
        """
        self.__instructor_repository = instructor_repository

    def __call__(self):
        return self.__instructor_repository.all()
