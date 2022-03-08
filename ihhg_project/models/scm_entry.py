from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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
            if rec.project_id.scm_entry_id:
                raise ValidationError(_("Project %s his already associated to an SCM: %s", rec.project_id.name, rec.project_id.scm))
