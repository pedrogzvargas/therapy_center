from marshmallow import Schema, fields


class CustomerSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    second_last_name = fields.Str(required=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class SearchCustomerSchema(Schema):
    page = fields.Int()
    limit = fields.Int()
    total = fields.Int()
    pages = fields.Int()
    results = fields.Nested(CustomerSchema, many=True)
