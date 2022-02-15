from odoo import models, fields, api


class Package (models.Model):
    _name = 'ihh.package'
    _description = 'Package'

    name = fields.Char(string='Package')
    item_total = fields.Integer(compute='_compute_item_total', string='Total Item (per Package)')
    channel_id = fields.Many2one('ihh.channel', string='Channel')

    # Count total number of items per package
    @api.depends('name')
    def _compute_item_total(self):
        for package in self:
            package.item_total = self.env['ihh.item'].search_count([('package_id', '=', package.name)])
