
from odoo import models, fields


class ItemTags(models.Model):
    _name = "item.tags"
    _description = "Item Tags"

    name = fields.Char(string='Name')
