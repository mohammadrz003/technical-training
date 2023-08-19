from odoo import api, fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    # ---------------------------------------- Action methods ------------------------------------
    def action_set_state_sold(self):
        invoice_values = {}
        for estate_property in self:
            invoice_values['partner_id'] = estate_property.buyer_id.id
            invoice_values['move_type'] = 'out_invoice'
            invoice_values['journal_id'] = self.env["account.journal"].search([("type", "=", "sale")], limit=1).id
            invoice_values['invoice_line_ids'] = [
                Command.create({
                    'name': estate_property.name,
                    'quantity': 1,
                    'price_unit': estate_property.selling_price * (6 / 100)
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        self.env['account.move'].create(invoice_values)
        return super(EstateProperty, self).action_set_state_sold()
