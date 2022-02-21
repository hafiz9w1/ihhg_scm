from datetime import datetime
from odoo import models, fields


class ItemLine (models.Model):
    _name = 'ihh.item.line'
    _description = 'Item_line'
    _rec_name = "item_id"

    item_id = fields.Many2one('ihh.item', string='Item')
    scm_id = fields.Many2one('scm.entry', string='SCM Reference', readonly=True, ondelete='cascade', index=True, copy=False)
    package_id = fields.Many2one(string='Package', readonly=True, store=True, related='item_id.package_id')
    channel_id = fields.Many2one(string='Channel', readonly=True, store=True, related='item_id.package_id.channel_id')
    item_date_from = fields.Datetime(string='Date From', default=datetime.now())
    item_date_to = fields.Datetime(string='Date To', default=datetime.now())
    product_id = fields.Many2one('product.product', string='POSM Item ID')
    dimension = fields.Char(string='Dimension')
    shipping_allocating = fields.Selection([
        ('shipping', 'Shipping'),
        ('allocating', 'Allocating')
    ], string='Shipping / Allocating')
    product_uom_id = fields.Many2one('uom.uom', string='UoM')
    quantity = fields.Float(string='Quantity', default=0.0)
    item_tags_ids = fields.Many2many('item.tags', string='Brand Name')
    sequence = fields.Integer(string='Sequence', readonly=True, default=10)
    state = fields.Selection(related='scm_id.state', string='SCM Status', readonly=True, copy=False, store=True)
