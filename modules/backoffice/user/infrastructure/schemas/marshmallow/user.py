from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    password = fields.Str()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
