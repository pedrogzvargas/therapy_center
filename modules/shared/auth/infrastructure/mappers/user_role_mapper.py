from sqlalchemy_models import UserRoleModel
from modules.shared.auth.domain.entities import UserRole


class UserRoleMapper:

    @staticmethod
    def to_model(entity: UserRole) -> UserRoleModel:
        model = UserRoleModel()
        model.id = entity.id
        model.user_id = entity.user_id
        model.role_id = entity.role_id
        model.is_active = entity.is_active
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def to_domain(model: UserRoleModel) -> UserRole:
        return UserRole(
            id=model.id,
            user_id=model.user_id,
            role_id=model.role_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
