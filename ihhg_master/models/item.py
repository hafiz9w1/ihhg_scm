from odoo import models, fields


class Item (models.Model):
    _name = 'ihh.item'
    _description = 'Item'

    name = fields.Char(string='Item')
    package_id = fields.Many2one('ihh.package', string='Package')
