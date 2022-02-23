from datetime import timedelta, datetime
from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    scm_entry_id = fields.Many2one('scm.entry', string='SCM')

    # Add field in project to capture deadline (Delivery Date) for project
    project_date_deadline = fields.Datetime(string='Delivery Date', tracking=True)


class Task(models.Model):
    _inherit = "project.task"

    # Add field in project task to capture project_offset (Offset)
    project_offset = fields.Integer(string='Offset', default=0)

    # Make date_deadline a computed field
    date_deadline = fields.Datetime(compute='_compute_date_deadline', tracking=True, store=True, string='Deadline')

    # The Deadline of all tasks  = (Delivery Date - (Offset * 7)) set from creating a project.
    @api.depends('project_offset', 'project_id.project_date_deadline')
    def _compute_date_deadline(self):
        for task in self:
            if not task.project_id.project_date_deadline:
                task.project_id.project_date_deadline = datetime.now()

            if not task.project_offset:
                task.project_offset = 0
            project_offset_delta = timedelta(days=(task.project_offset * 7))
            task.date_deadline = task.project_id.project_date_deadline - project_offset_delta
