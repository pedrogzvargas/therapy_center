from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    price = fields.Str()
    is_active = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class SearchProductSchema(Schema):
    page = fields.Int()
    limit = fields.Int()
    total = fields.Int()
    pages = fields.Int()
    results = fields.Nested(ProductSchema, many=True)
