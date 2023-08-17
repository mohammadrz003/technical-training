from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "The tags of estate properties"
    _order = "name"

    name = fields.Char(required=True)
    _sql_constraints = [
        ("name_uniq", "unique(name)", "The name of a tag must be unique")
    ]
    color = fields.Integer()
