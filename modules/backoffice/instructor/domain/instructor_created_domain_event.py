from modules.shared.bus.event.domain import DomainEvent


class InstructorCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id,
        user_id,
        name,
        last_name,
        second_last_name,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__user_id = user_id
        self.__name = name
        self.__last_name = last_name
        self.__second_last_name = second_last_name

    def event_name(self):
        return "backoffice.instructor.created"

    def to_primitives(self):
        return dict(
            aggregate_id=self.__aggregate_id,
            user_id=self.__user_id,
            name=self.__name,
            last_name=self.__last_name,
            second_last_name=self.__second_last_name,
            event_id=self.__event_id,
            occurred_on=self.__occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return InstructorCreatedDomainEvent(
            aggregate_id=aggregate_id,
            user_id=body.get("user_id"),
            name=body.get("name"),
            last_name=body.get("last_name"),
            second_last_name=body.get("second_last_name"),
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def second_last_name(self):
        return self.__second_last_name
