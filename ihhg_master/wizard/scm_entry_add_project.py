from unicodedata import name
from odoo import models, fields, _


class ScmEntryAddProject(models.TransientModel):
    _name = "scm.entry.add.project"
    _description = "Add project to scm"

    scm_id = fields.Many2one(comodel_name="scm.entry")
    project_selection = fields.Selection([
        ('select_existing_project', 'Select Existing Project'),
        ('create_project_from_template', 'Create Project From Template'),
    ], string='Project Selection', default='select_existing_project')
    project_exist_id = fields.Many2one('project.project', string='Select Existing Project', domain=[('scm_entry_id', '=', False)])
    project_template_id = fields.Many2one('project.project', string='Create Project From Template', domain=[('is_template', '=', True)])
    project_name_new = fields.Char(string='Enter Project Name')

    def action_confirm(self):
        self.ensure_one()
        for rec in self:
            if rec.project_exist_id:
                rec.scm_id.project_id = rec.project_exist_id
                rec.project_exist_id.scm_entry_id = rec.scm_id
            else:
                if rec.project_template_id:
                    rec.scm_id.project_id = self.env['project.project'].copy_project_as_template([('id', '=', rec.project_template_id.id, 'name', '=', rec.project_template_id.name)])
