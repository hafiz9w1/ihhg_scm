from odoo import models, fields


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    scm_entry_id = fields.Many2one('scm.entry', string='SCM Reference')

    # Log message in SCM chatter
    def action_confirm(self):
        res = super(ApprovalRequest, self).action_confirm()

        for rec in self:
            if rec.scm_entry_id:
                rec.scm_entry_id.message_post(body="Approval Request submitted for this SCM entry", subject="SCM Approval")

        return res
