import datetime
from asyncio import tasks
from numpy import record
from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    selection_criteria_id = fields.Many2many('selection.criteria', string='Selection Criteria')
    scm_entry_id = fields.Many2one('scm.entry', string='SCM')

    # Add field in project to capture deadline for project
    project_date_deadline = fields.Date(string='Deadline', tracking=True)

    # Function for updating date_deadline - Get number of days between previous and current project_date_deadline and add to task under the project
    def write(self, vals):
        previous_project_date_deadline = {}
        for rec in self:
            previous_project_date_deadline[rec.id] = rec.project_date_deadline
        res = super(Project, self).write(vals)
        for rec in self:
            if not rec.project_date_deadline or not previous_project_date_deadline[rec.id]:
                continue
            date_delta = rec.project_date_deadline - previous_project_date_deadline[rec.id]
            for do_task in rec.task_ids:
                do_task.write({'date_deadline': do_task.date_deadline + date_delta})
        return res
