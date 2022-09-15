from marshmallow import Schema, fields


class OrderOutputSchema(Schema):
    id = fields.Integer(dump_only=True)
    order_number = fields.Integer(dump_only=True)
    delivery_date = fields.Date(format="%d.%m.%Y", dump_only=True)
    cost = fields.Decimal(dump_only=True)
    cost_rub = fields.Decimal(dump_only=True)
