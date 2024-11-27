from marshmallow import Schema, fields


class ServiceSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    price = fields.Str()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
