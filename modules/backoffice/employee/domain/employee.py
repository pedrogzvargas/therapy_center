from modules.shared.aggregate_root.domain import AggregateRoot
from .employee_created_domain_event import EmployeeCreatedDomainEvent
from .employee_patched_domain_event import EmployeePatchedDomainEvent


class Employee(AggregateRoot):
    """
    Employee entity
    """

    def __init__(self, id, user_id, name, last_name, created_at, updated_at, second_last_name=None):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.second_last_name = second_last_name
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id, user_id, name, last_name, created_at=None, updated_at=None, second_last_name=None):
        employee = Employee(
            id=id,
            user_id=user_id,
            name=name,
            last_name=last_name,
            second_last_name=second_last_name,
            created_at=created_at,
            updated_at=updated_at,
        )

        employee.record(
            EmployeeCreatedDomainEvent(
                aggregate_id=id,
                user_id=user_id,
                name=name,
                last_name=last_name,
                second_last_name=second_last_name,
            )
        )

        return employee

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

        self.record(
            EmployeePatchedDomainEvent(
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
