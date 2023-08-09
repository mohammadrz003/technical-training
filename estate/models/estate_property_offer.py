from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "The offers of estate properties"

    # Basic
    price = fields.Float()
    status = fields.Selection(
        selection=[("Accepted", "Accepted"), ("Refused", "Refused")],
        copy=False,
    )

    # Relational
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Computed
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # ---------------------------------------- Compute methods ------------------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_set_status_accepted(self):
        if "Accepted" in self.mapped('property_id.offer_ids.status'):
            raise UserError("An offer has already been accepted")
        for offer in self:
            offer.status = "Accepted"
        return self.mapped("property_id").write(
            {
                "state": "Offer_Accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id
            }
        )

    def action_set_status_refused(self):
        for offer in self:
            offer.status = "Refused"
        return True
