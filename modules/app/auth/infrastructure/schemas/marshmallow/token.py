from marshmallow import Schema, fields


class TokenSchema(Schema):
    token = fields.Str()
