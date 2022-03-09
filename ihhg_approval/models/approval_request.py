from odoo import models, fields


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    scm_entry_id = fields.Many2one('scm.entry', string='SCM Reference')
    has_scm = fields.Selection(related='category_id.has_scm')

    # Log message in SCM chatter when approval submitted
    def action_confirm(self):
        res = super(ApprovalRequest, self).action_confirm()

        for rec in self:
            if rec.scm_entry_id:
                rec.scm_entry_id.message_post(body="An Approval Request has been submitted for this SCM entry", subject="SCM Approval - Request")

        return res

    # Log message in SCM chatter when request approved
    def action_approve(self):
        res = super(ApprovalRequest, self).action_approve()

        for rec in self:
            if rec.scm_entry_id:
                rec.scm_entry_id.message_post(body="Approval Request submitted for this SCM entry has been approved", subject="SCM Approval - Approved")

        return res

    # Log message in SCM chatter when request refused
    def action_refuse(self):
        res = super(ApprovalRequest, self).action_refuse()

        for rec in self:
            if rec.scm_entry_id:
                rec.scm_entry_id.message_post(body="Approval Request submitted for this SCM entry has been refused", subject="SCM Approval - Refused")

        return res

    # Log message in SCM chatter when request cancelled
    def action_cancel(self):
        res = super(ApprovalRequest, self).action_cancel()

        for rec in self:
            if rec.scm_entry_id:
                rec.scm_entry_id.message_post(body="Approval Request submitted for this SCM entry has been cancelled", subject="SCM Approval - Cancelled")

        return res

    # Log message in SCM chatter when request cancelled
    def action_withdraw(self):
        res = super(ApprovalRequest, self).action_withdraw()

        for rec in self:
            if rec.scm_entry_id:
                rec.scm_entry_id.message_post(body="Approval Request submitted for this SCM entry has been withdrawn", subject="SCM Approval - Withdrawn")

        return res
