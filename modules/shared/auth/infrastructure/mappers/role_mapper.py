from sqlalchemy_models import RoleModel
from modules.shared.auth.domain.entities import Role


class RoleMapper:

    @staticmethod
    def to_model(entity: Role) -> RoleModel:
        model = RoleModel()
        model.id = entity.id
        model.name = entity.name
        model.is_active = entity.is_active
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def to_domain(model: RoleModel) -> Role:
        return Role(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
