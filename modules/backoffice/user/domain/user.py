from modules.shared.aggregate_root.domain import AggregateRoot
from .user_created_domain_event import UserCreatedDomainEvent
from .user_patched_domain_event import UserPatchedDomainEvent


class User(AggregateRoot):
    """
    User entity
    """

    def __init__(self, id, username, password, is_active, created_at, updated_at):
        super().__init__()
        self.id = id
        self.username = username
        self.password = password
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id, username, password, is_active, created_at=None, updated_at=None):
        user = User(
            id=id,
            username=username,
            password=password,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
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
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
