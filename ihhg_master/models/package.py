from odoo import models, fields


class Package (models.Model):
    _name = 'ihh.package'
    _description = 'Package'

    name = fields.Char(string='Package')
    quantity = fields.Integer(string='Quantity')
    channel_id = fields.Many2one('ihh.channel', string='Channel')
