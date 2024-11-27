from marshmallow import Schema, fields


class PaymentMethodSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
