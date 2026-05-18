from sqlalchemy_models import PaymentMethodModel
from modules.backoffice.payment_method.domain import PaymentMethod


class PaymentMethodMapper:

    @staticmethod
    def to_model(entity: PaymentMethod) -> PaymentMethodModel:
        model = PaymentMethodModel()
        model.id = entity.id
        model.name = entity.name
        model.is_active = entity.is_active
        return model

    @staticmethod
    def to_domain(model: PaymentMethodModel) -> PaymentMethod:
        return PaymentMethod(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
