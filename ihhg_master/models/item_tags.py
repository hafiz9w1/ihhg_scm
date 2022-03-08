
from odoo import models, fields


class ItemTags(models.Model):
    _name = "ihh.item.tag"
    _description = "Item Tags"

    name = fields.Char(string='Name', translate=True)
    active = fields.Boolean('Active', default=True)
