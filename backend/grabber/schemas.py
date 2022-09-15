from marshmallow import Schema, fields


class OrderInputSchema(Schema):
    id = fields.Integer(required=True)
    order_number = fields.Integer(required=True)
    delivery_date = fields.Date(format="%d.%m.%Y")
    cost = fields.Decimal(required=True)
    # cost_rub = fields.Integer(dump_only=True)
