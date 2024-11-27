from modules.shared.aggregate_root.domain import AggregateRoot
from .instructor_created_domain_event import InstructorCreatedDomainEvent
from .instructor_patched_domain_event import InstructorPatchedDomainEvent


class Instructor(AggregateRoot):
    """
    Instructor entity
    """

    def __init__(self, id, user_id, name, last_name, second_last_name=None):
        self.__id = id
        self.__user_id = user_id
        self.__name = name
        self.__last_name = last_name
        self.__second_last_name = second_last_name

    @staticmethod
    def create(id, user_id, name, last_name, second_last_name=None):
        instructor = Instructor(
            id=id,
            user_id=user_id,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
        )

        instructor.record(
            InstructorCreatedDomainEvent(
                aggregate_id=id,
                user_id=user_id,
                name=name,
                last_name=last_name,
                second_last_name=second_last_name,
            )
        )

        return instructor

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            InstructorPatchedDomainEvent(
                aggregate_id=self.id,
                data=data,
            )
        )

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            last_name=self.last_name,
            second_last_name=self.second_last_name,
        )

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def second_last_name(self):
        return self.__second_last_name

    @second_last_name.setter
    def second_last_name(self, second_last_name):
        self.__second_last_name = second_last_name
