from odoo import models, fields, api


class Package (models.Model):
    _name = 'ihh.package'
    _description = 'Package'

    name = fields.Char(string='Packing ID')
    long_name = fields.Char(string="Package name")
    channel_id = fields.Many2one('ihh.channel', string='Channel')
    item_ids = fields.One2many(comodel_name="ihh.package.item", inverse_name="package_id")
    item_total = fields.Integer(compute='_compute_item_total', string='Total Item (per Package)')
    delivery_address_ids = fields.One2many(comodel_name="res.partner", inverse_name="package_id")
    secondary_address_ids = fields.One2many(comodel_name="ihh.package.secondary.address", inverse_name="package_id")
    naming_convention = fields.Selection([
        ('LW', 'LW'),
        ('DY', 'DY'),
        ('SCMART', 'SCMART'),
    ], default="LW", string='Naming Convention')
    quantity = fields.Integer()
    active = fields.Boolean('Active', default=True)

    @api.depends('item_ids')
    def _compute_item_total(self):
        for package in self:
            package.item_total = len(package.item_ids)
