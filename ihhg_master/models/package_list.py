
from odoo import models, fields


class SelectionCriterium(models.Model):
    _name = "ihh.package.list"
    _description = "Package List"

    name = fields.Char(string='Name')
    package_id = fields.Many2one('ihh.package', string='Package')
