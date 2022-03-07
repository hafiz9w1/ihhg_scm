from datetime import datetime, timedelta
from odoo import models, fields, api


class Task(models.Model):
    _inherit = "project.task"

    member_ids = fields.Many2many(related="project_id.member_ids")
    user_ids = fields.Many2many(domain="[('id', 'in', member_ids)]")

    def change_deadline_from_scm(self, delta):
        for rec in self:
            vals = {}
            if rec.planned_date_begin:
                vals.update({
                    "planned_date_begin": rec.planned_date_begin - delta
                })

            if rec.planned_date_end:
                vals.update({
                    "planned_date_end": rec.planned_date_end - delta
                })

            if rec.date_deadline:
                vals.update({
                    "date_deadline": rec.date_deadline - delta
                })

            if vals:
                rec.write(vals)
            # No need already catch as project_task
            # rec.child_ids.change_deadline_from_scm(delta)
