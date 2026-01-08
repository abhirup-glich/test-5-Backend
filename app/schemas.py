from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    name = fields.String(required=True)
    unique_id = fields.String(required=True)
    course = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class AdminLoginInitSchema(Schema):
    email = fields.Email(required=True)

class AdminLoginVerifySchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    otp = fields.String(required=True, validate=validate.Length(equal=6))

class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8))

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String()
    unique_id = fields.String()
    course = fields.String()
    email = fields.Email()
    created_at = fields.DateTime(dump_only=True)

class AuthResponseSchema(Schema):
    access_token = fields.String()
    user = fields.Nested(UserSchema)

class UserResponseSchema(Schema):
    user = fields.Nested(UserSchema)
