from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    package_ids = fields.Many2many(comodel_name='ihh.package')
