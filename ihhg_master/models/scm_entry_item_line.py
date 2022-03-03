from datetime import datetime

from odoo import models, fields, api


class ItemLine (models.Model):
    _name = 'scm.entry.item.line'
    _description = 'Item_line'

    name = fields.Char(string='Name', compute="_compute_name")
    item_id = fields.Many2one('product.template', string='Item')
    sequence = fields.Integer(string='Sequence', readonly=True, default=10)
    product_id = fields.Many2one('product.product', string='POSM Item ID', readonly=True)
    scm_id = fields.Many2one('scm.entry', string='SCM Reference', readonly=True, ondelete='cascade', index=True)
    allowed_channel_ids = fields.Many2many('ihh.channel', string='Allowed Channel', related="scm_id.channel_ids")
    scm_package_line_id = fields.Many2one('scm.entry.package.line')
    package_id = fields.Many2one(string='Package', readonly=True, store=True, related='item_id.package_id')
    channel_id = fields.Many2one(string='Channel', readonly=True, store=True, related='item_id.package_id.channel_id')
    item_date_from = fields.Date(string='Date From', inverse='_inverse_item_date_from', compute='_compute_item_date_from', store=True)
    item_date_to = fields.Date(string='Date To', inverse='_inverse_item_date_to', compute='_compute_item_date_to', store=True)
    dimension = fields.Char(string='Dimension')
    shipping_allocating = fields.Selection([
        ('shipping', 'Shipping'),
        ('allocating', 'Allocating')
    ], string='Shipping / Allocating')
    product_uom_id = fields.Many2one('uom.uom', string='UoM')
    quantity = fields.Integer(string='Quantity', compute="_compute_quantity")
    item_tags_ids = fields.Many2many('ihh.item.tag', string='Brand Name')
    state = fields.Selection(related='scm_id.state', string='SCM Status', readonly=True, copy=False, store=True)

    @api.depends('scm_package_line_id.quantity', 'item_id.package_quantity')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.scm_package_line_id.quantity * rec.item_id.package_quantity

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

    # When creating item_id, automatically create a package_id if it doesn't exist
    @api.model
    def create(self, vals):
        res = super(ItemLine, self).create(vals)

        packages_line = self.env['scm.entry.package.line'].search([('package_id', 'in', res.package_id.ids), ('scm_id', 'in', res.scm_id.ids)]).package_id

        if res.item_id:
            if res.package_id not in packages_line:

                package = self.env['scm.entry.package.line'].create({
                    'package_id': res.package_id.id,
                    'scm_id': res.scm_id.id,
                    'scm_entry_item_line_id': res.item_id.ids,
                })
                res.scm_package_line_id = package

            return res

    # Delete package line when Item line is removed
    def unlink(self):
        scm_package_line_to_delete = self.env['scm.entry.package.line'].search([('id', 'in', self.scm_package_line_id.ids)])

        for rec in self:
            if rec.scm_package_line_id:

                res = super(ItemLine, self).unlink()
                scm_package_line_to_delete.unlink()
        return res

    # Select SCM date_from for Item item_date_from
    @api.depends('scm_id.date_from')
    def _compute_item_date_from(self):
        for rec in self:
            rec.item_date_from = rec.scm_id.date_from

    def _inverse_item_date_from(self):
        pass

    # Select SCM date_to for Item item_date_to
    @api.depends('scm_id.date_to')
    def _compute_item_date_to(self):
        for rec in self:
            rec.item_date_to = rec.scm_id.date_to

    def _inverse_item_date_to(self):
        pass
