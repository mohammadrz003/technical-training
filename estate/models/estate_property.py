from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The properties for an estate"
    _order = "id desc"

    # Basic
    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", copy=False, default=datetime.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)

    _sql_constraints = [
        ('check_positive', 'CHECK(expected_price >= 0)',
         'The expected price must be strictly positive')
    ]

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
        string="Status"
    )
    active = fields.Boolean(default=True)

    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, string="Salesman"
    )
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed
    total_area = fields.Integer(compute="_compute_total_area", readonly=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    # ---------------------------------------- Compute methods ------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids.mapped("price"):
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = None

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # ---------------------------------------- Action methods ------------------------------------

    def action_set_state_cancel(self):
        for record in self:
            if record.state == "Sold":
                raise UserError("A sold property cannot be canceled")
            else:
                record.state = "Canceled"
        return True

    def action_set_state_sold(self):
        for record in self:
            if record.state == "Canceled":
                raise UserError("A canceled property cannot be set as sold")
            else:
                record.state = "Sold"
        return True

    # ---------------------------------------- Constraints methods ------------------------------------

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_rounding=0.01)
                    and float_compare(record.selling_price, record.expected_price * 90.0 / 100.0,
                                      precision_rounding=0.01) < 0):
                raise ValidationError(
                    "selling price cannot be lower than 90% of the expected price. "
                    + "reduce the expected price if you want to accept this offer")
