from modules.shared.bus.event.domain import DomainEvent


class UserCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id,
        username,
        password,
        is_active,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__username = username
        self.__password = password
        self.__is_active = is_active

    def event_name(self):
        return "backoffice.user.created"

    def to_primitives(self):
        return dict(
            aggregate_id=self.__aggregate_id,
            username=self.__username,
            password=self.__password,
            is_active=self.__is_active,
            event_id=self.__event_id,
            occurred_on=self.__occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return UserCreatedDomainEvent(
            aggregate_id=aggregate_id,
            username=body.get("username"),
            password=body.get("password"),
            is_active=body.get("is_active"),
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def is_active(self):
        return self.__is_active
