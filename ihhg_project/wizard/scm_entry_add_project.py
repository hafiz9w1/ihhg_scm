from odoo import models, fields, _


class ScmEntryAddProject(models.TransientModel):
    _name = "scm.entry.add.project"
    _description = "Add project to scm"

    scm_id = fields.Many2one(comodel_name="scm.entry")
    project_selection = fields.Selection([
        ('select_existing_project', 'Select Existing Project'),
        ('create_project_from_template', 'Create Project From Template'),
    ], string='Project Selection', default='select_existing_project', required=True)
    project_exist_id = fields.Many2one('project.project', string='Select Existing Project', domain=[('scm_entry_id', '=', False), ('is_template', '!=', True)])
    project_template_id = fields.Many2one('project.project', string='Create Project From Template', domain=[('is_template', '=', True)])
    project_name_new = fields.Char(string='Enter Project Name')

    def action_confirm(self):
        self.ensure_one()
        if self.project_selection == "select_existing_project":
            project = self.project_exist_id
        else:
            project = self.project_template_id._create_project_from_template(name=self.project_name_new)

        project.change_deadline_from_scm(self.scm_id.date_from)
        self.scm_id.write({
            "project_id": project.id
        })
