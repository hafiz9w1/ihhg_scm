
from odoo import models, fields


class SelectionCriterium(models.Model):
    _name = "selection.criteria"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Selection Criteria"

    name = fields.Char(string='Name')
