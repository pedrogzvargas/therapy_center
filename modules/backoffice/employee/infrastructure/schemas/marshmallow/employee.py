from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    second_last_name = fields.Str(required=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class SearchEmployeeSchema(Schema):
    page = fields.Int()
    limit = fields.Int()
    total = fields.Int()
    pages = fields.Int()
    results = fields.Nested(EmployeeSchema, many=True)
