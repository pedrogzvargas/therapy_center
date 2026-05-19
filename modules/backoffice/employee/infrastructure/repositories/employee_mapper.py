from sqlalchemy_models import EmployeeModel
from modules.backoffice.employee.domain import Employee


class EmployeeMapper:

    @staticmethod
    def to_model(entity: Employee) -> EmployeeModel:
        model = EmployeeModel()
        model.id = entity.id
        model.user_id = entity.user_id
        model.name = entity.name
        model.last_name = entity.last_name
        model.second_last_name = entity.second_last_name
        return model

    @staticmethod
    def to_domain(model: EmployeeModel) -> Employee:
        return Employee(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            last_name=model.last_name,
            second_last_name=model.second_last_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
