from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The properties for an estate"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", copy=False, default=datetime.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("North", "North"),
            ("South", "South"),
            ("East", "East"),
            ("West", "West"),
        ]
    )
    state = fields.Selection(
        selection=[
            ("New", "New"),
            (
                "Offer_Received",
                "Offer Received",
            ),
            ("Offer_Accepted", "Offer Accepted"),
            ("Sold", "Sold"),
            ("Canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="New",
    )
    active = fields.Boolean(default=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
