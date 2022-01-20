
from odoo import models, fields


class SelectionCriterium(models.Model):
    _name = "selection.criteria"
    _description = "Selection Criteria"

    name = fields.Char(string='Name')
