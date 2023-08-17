from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The types of estate properties"
    _order = "sequence, name"

    # Basic
    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "The name of a type must be unique")
    ]

    sequence = fields.Integer("Sequence")

    # Relational
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    login_user_group = fields.Boolean(compute="_check_login_user_group")

    @api.depends()
    def _check_login_user_group(self):
        user_pool = self.env['res.users']
        user = user_pool.browse(self._uid)
        desired_user_gr = user.has_group('estate.group_estate_property_type_manager')
        return desired_user_gr
