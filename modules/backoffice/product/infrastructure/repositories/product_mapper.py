from sqlalchemy_models import ProductModel
from modules.backoffice.product.domain import Product


class ProductMapper:

    @staticmethod
    def to_model(entity: Product) -> ProductModel:
        model = ProductModel()
        model.id = entity.id
        model.name = entity.name
        model.description = entity.description
        model.price = entity.price
        model.is_active = entity.is_active
        return model

    @staticmethod
    def to_domain(model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
