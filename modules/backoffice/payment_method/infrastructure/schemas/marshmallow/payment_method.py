from marshmallow import Schema, fields


class PaymentMethodSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class SearchPaymentMethodSchema(Schema):
    page = fields.Int()
    limit = fields.Int()
    total = fields.Int()
    pages = fields.Int()
    results = fields.Nested(PaymentMethodSchema, many=True)
