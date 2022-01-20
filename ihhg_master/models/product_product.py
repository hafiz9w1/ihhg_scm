
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    originating_project = fields.Many2one(string='Originating Project') # Do not understand the purpose of this
