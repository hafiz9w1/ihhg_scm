from odoo import models, fields

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    has_scm = fields.Selection(CATEGORY_SELECTION, string="Has SCM", default="no", required=True)
