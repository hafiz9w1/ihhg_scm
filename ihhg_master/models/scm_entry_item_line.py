from datetime import datetime
from odoo import models, fields, api


class ItemLine (models.Model):
    _name = 'scm.entry.item.line'
    _description = 'Item_line'

    name = fields.Char(string='Name', compute="_compute_name")
    sequence = fields.Integer(string='Sequence', readonly=True, default=10)
    item_id = fields.Many2one('product.template', string='Item')
    product_id = fields.Many2one('product.product', string='POSM Item ID', readonly=True)
    scm_id = fields.Many2one('scm.entry', string='SCM Reference', readonly=True, ondelete='cascade', index=True)
    allowed_channel_ids = fields.Many2many('ihh.channel', related="scm_id.channel_ids")
    scm_package_line_id = fields.Many2one('scm.entry.package.line')
    package_id = fields.Many2one(string='Package', readonly=True, store=True, related='item_id.package_id')
    channel_id = fields.Many2one(string='Channel', readonly=True, store=True, related='item_id.package_id.channel_id')
    item_date_from = fields.Date(string='Date From', default=lambda r: fields.Date.context_today(r))
    item_date_to = fields.Date(string='Date To', default=lambda r: fields.Date.context_today(r))
    dimension = fields.Char(string='Dimension')
    shipping_allocating = fields.Selection([
        ('shipping', 'Shipping'),
        ('allocating', 'Allocating')
    ], string='Shipping / Allocating')
    product_uom_id = fields.Many2one('uom.uom', string='UoM')
    quantity = fields.Float(string='Quantity', compute="_compute_quantity")
    item_tags_ids = fields.Many2many('ihh.item.tag', string='Brand Name')
    state = fields.Selection(related='scm_id.state', string='SCM Status', readonly=True, copy=False, store=True)

    @api.depends('scm_package_line_id.quantity', 'product_id.package_quantity')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.scm_package_line_id.quantity * rec.product_id.package_quantity

    # TODO: implement more complexe logic if needed
    @api.depends('item_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.item_id.name

    # Function to append Brand Name to item name in Visibility calendar
    def name_get(self):
        res = []
        for item in self:
            name_array = [item.item_id.name] + item.item_tags_ids.mapped('name')
            name = ' - '.join(name_array)
            res.append((item.id, name))
        return res
