from sqlalchemy_models import UserModel
from modules.backoffice.user.domain import User


class UserMapper:

    @staticmethod
    def to_model(entity: User) -> UserModel:
        model = UserModel()
        model.id = entity.id
        model.email = entity.email
        model.username = entity.username
        model.password = entity.password
        model.is_active = entity.is_active
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            password=model.password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
