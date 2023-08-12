from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The types of estate properties"
    _order = "sequence, name"

    # Basic
    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence")

    # Relational
    property_ids = fields.One2many('estate.property', 'property_type_id')
