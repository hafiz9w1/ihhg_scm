from odoo import models, fields, api


class Package (models.Model):
    _name = 'ihh.package.secondary.address'
    _description = 'package Secondary Address'
    _rec_name = 'address_id'

    package_id = fields.Many2one(comodel_name='ihh.package', string='Channel')
    address_id = fields.Many2one(comodel_name="res.partner")
    backup_quantity = fields.Integer()
