from odoo import models, fields


class Package (models.Model):
    _name = 'ihh.package.item'
    _description = 'Package Item'

    name = fields.Char(related='product_template_id.posm_item_id')
    product_template_id = fields.Many2one(
        comodel_name='product.template',
        string='Item',
    )
    package_id = fields.Many2one('ihh.package', string='Package')
    package_name = fields.Char(related='package_id.long_name')
    channel_id = fields.Many2one(
        'ihh.channel',
        string='Channel',
        related='package_id.channel_id',
        store=True,
    )
    package_quantity = fields.Integer(string='Quantity')
