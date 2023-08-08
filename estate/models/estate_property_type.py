from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The types of estate properties"

    name = fields.Char(required=True)
