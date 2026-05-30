from modules.shared.bus.event.domain import DomainEvent


class UserCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id,
        email,
        username,
        password,
        is_active,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__aggregate_id= aggregate_id
        self.__email = email
        self.__username = username
        self.__password = password
        self.__is_active = is_active

    def event_name(self):
        return "backoffice.user.created"

    def to_primitives(self):
        return dict(
            email=self.email,
            username=self.__username,
            password=self.__password,
            is_active=self.__is_active,
            aggregate_id=self.aggregate_id,
            event_id=self.event_id,
            event_name=self.event_name(),
            occurred_on=self.occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return UserCreatedDomainEvent(
            aggregate_id=aggregate_id,
            email=body.get("email"),
            username=body.get("username"),
            password=body.get("password"),
            is_active=body.get("is_active"),
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def email(self):
        return self.__email

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def is_active(self):
        return self.__is_active
