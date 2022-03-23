from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SCMEntry(models.Model):
    _inherit = "scm.entry"

    date_from = fields.Date(inverse="_inverse_date_from")

    def _inverse_date_from(self):
        """
        On save the date_from - we are updating the project deadline if needed
        """
        if self.project_id:
            self.project_id.change_deadline_from_scm(self.date_from)

    @api.constrains('project_id')
    def _check_scm_unicity_project(self):
        for rec in self:
            if rec.project_id.scm_entry_id and rec.project_id.scm_entry_id != rec:
                raise ValidationError(_("Project %s his already associated to an SCM: %s", rec.project_id.name, rec.project_id.scm_entry_id.name))

    # Add project to SCM
    def action_add_project(self):
        self.ensure_one()
        if not self.date_from:
            raise UserError(_('Please input Campaign Duration'))

        add_project = self.env['scm.entry.add.project'].create({
            "scm_id": self.id
        })

        context = dict(self.env.context)

        return {
            'name': _('Select Project'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('ihhg_project.view_scm_entry_add_project').id,
            'res_model': 'scm.entry.add.project',
            'res_id': add_project.id,
            'target': 'new',
            'context': context
        }
