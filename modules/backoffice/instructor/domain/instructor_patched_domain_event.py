from modules.shared.bus.event.domain import DomainEvent


class InstructorPatchedDomainEvent(DomainEvent):

    def __init__(self, aggregate_id, data, event_id=None, occurred_on=None):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__data = data

    def event_name(self):
        return "backoffice.instructor.patched"

    def to_primitives(self):
        return dict(
            aggregate_id=self.__aggregate_id,
            data=self.__data,
            event_id=self.__event_id,
            occurred_on=self.__occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return InstructorPatchedDomainEvent(
            aggregate_id=aggregate_id,
            data=body,
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def data(self):
        return self.__data
