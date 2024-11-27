from marshmallow import Schema, fields


class InstructorSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    second_last_name = fields.Str(required=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
