from marshmallow import Schema, fields, validate

from ORM import models


class Credentials(Schema):
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True)


class UserToCreate(Schema):
    email = fields.String(required=True, validate=validate.Email())
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, min=5)


class UserData(Schema):
    id = fields.Integer()
    username = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.String()
    phone = fields.String()
    userAuthStatus = fields.String(validate=validate.OneOf([i.value for i in list(models.UserStatus)]))


class UserListFilter(Schema):
    email = fields.String(validate=validate.Email())
    firstName = fields.String()
    lastName = fields.String()


class WalletToCreate(Schema):
    name = fields.String(required=True)
    currency = fields.String(required=True, validate=validate.OneOf([i.value for i in list(models.Currency)]))
    user_id = fields.Integer(required=True)


class WalletData(Schema):
    user_id = fields.Integer()
    balance = fields.Integer()
    name = fields.String()
    currency = fields.String(validate=validate.OneOf([i.value for i in list(models.Currency)]))


class WalletListFilter(Schema):
    user_id = fields.Integer()


class Transaction(Schema):
    wallet_recipient = fields.String(required=True)
    cost = fields.Integer(required=True)


class Response(Schema):
    code = fields.Integer()
    type = fields.String(default="OK")
    message = fields.String()
