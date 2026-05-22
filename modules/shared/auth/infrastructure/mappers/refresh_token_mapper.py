from sqlalchemy_models import RefreshTokenModel
from modules.shared.auth.domain.entities import RefreshToken


class RefreshTokenMapper:

    @staticmethod
    def to_model(entity: RefreshToken) -> RefreshTokenModel:
        model = RefreshTokenModel()
        model.id = entity.id
        model.user_id = entity.user_id
        model.jti = entity.jti
        model.revoked = entity.revoked
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def to_domain(model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            jti=model.jti,
            revoked=model.revoked,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
