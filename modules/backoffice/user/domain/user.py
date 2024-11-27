from modules.shared.aggregate_root.domain import AggregateRoot
from .user_created_domain_event import UserCreatedDomainEvent
from .user_patched_domain_event import UserPatchedDomainEvent


class User(AggregateRoot):
    """
    User entity
    """

    def __init__(self, id, username, password, is_active):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__is_active = is_active

    @staticmethod
    def create(id, username, password, is_active):
        user = User(
            id=id,
            username=username,
            password=password,
            is_active=is_active,
        )

        user.record(
            UserCreatedDomainEvent(
                aggregate_id=id,
                username=username,
                password=password,
                is_active=is_active,
            )
        )

        return user

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            UserPatchedDomainEvent(
                aggregate_id=self.id,
                data=data,
            )
        )

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            password=self.password,
            is_active=self.is_active,
        )

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active):
        self.__is_active = is_active
