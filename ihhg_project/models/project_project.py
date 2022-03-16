from datetime import timedelta
from odoo import models, fields, _


class Project(models.Model):
    _inherit = 'project.project'

    is_template = fields.Boolean(default=False, copy=False)
    scm_entry_id = fields.Many2one('scm.entry', string='SCM', compute="_compute_scm_entry_id")
    date_from = fields.Date(string='SCM Campaign Start', related="scm_entry_id.date_from")
    date_to = fields.Date(string='SCM Campaign Stop', related="scm_entry_id.date_to")
    privacy_visibility = fields.Selection(default="followers")
    project_date_deadline = fields.Date(string='Delivery Date', tracking=True, required=True)

    member_ids = fields.Many2many(
        comodel_name='res.users',
        relation='project_user_rel',
        column1='project_id',
        column2='user_id',
        string='Project Members',
        help="""Project's members are users who can have an access to the tasks related to this project.""",
    )

    def _compute_scm_entry_id(self):
        for rec in self:
            rec.scm_entry_id = self.env['scm.entry'].search([('project_id', '=', rec.id)], limit=1).id

    # TODO - see refactor code for name function odoo issue
    def _map_tasks_default_valeus(self, task, project):
        res = super(Project, self)._map_tasks_default_valeus(task, project)
        res.update({
            "display_project_id": project.id
        })

        return res

    def map_tasks(self, new_project_id):
        """ [OVERWRITE] copy and map tasks from old to new project """
        project = self.browse(new_project_id)
        tasks = self.env['project.task']
        # We want to copy archived task, but do not propagate an active_test context key
        task_ids = self.env['project.task'].with_context(active_test=False).search([('project_id', '=', self.id)], order='parent_id').ids
        old_to_new_tasks = {}
        for task in self.env['project.task'].browse(task_ids):
            # preserve task name and stage, normally altered during copy
            defaults = self._map_tasks_default_valeus(task, project)
            if task.parent_id:
                # set the parent to the duplicated task
                defaults['parent_id'] = old_to_new_tasks.get(task.parent_id.id, False)
            new_task = task.copy(defaults)
            # If child are created before parent (ex sub_sub_tasks)
            new_child_ids = [old_to_new_tasks[child.id] for child in task.child_ids if child.id in old_to_new_tasks]
            # ############ OVERWRITE ############
            tasks.browse(new_child_ids).write({'parent_id': new_task.id, 'display_project_id': project.id})
            # ############ OVERWRITE ############
            old_to_new_tasks[task.id] = new_task.id
            tasks += new_task

        return project.write({'tasks': [(6, 0, tasks.ids)]})

    def change_deadline_from_scm(self, scm_start_date):
        self.ensure_one()
        self = self.with_context(date_auto_shift=False)
        theoric_deadline = scm_start_date - timedelta(weeks=2)
        delta = self.project_date_deadline - theoric_deadline
        vals = {
            "project_date_deadline": theoric_deadline,
        }

        if self.date_start:
            vals.update({
                "date_start": self.date_start - delta,

            })

        if self.date:
            vals.update({
                "date": self.date - delta,
            })
        self.tasks.change_deadline_from_scm(delta)
        self.write(vals)

    def _create_project_from_template(self, name=None):
        self.ensure_one()
        default = {
            'is_template': False
        }
        if name:
            default['name'] = name
        new_project = self.copy(default)

        return new_project

    def action_create_project_from_template(self):
        new_project = self._create_project_from_template()
        context = dict(self.env.context)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'target': 'current',
            'context': context
        }

    def action_create_template_from_project(self):
        self.ensure_one()
        new_project = self.copy({'is_template': True})
        new_project.write({
            "name": _("(TEMPLATE) %s", self.name)
        })
        context = dict(self.env.context)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'target': 'current',
            'context': context
        }

    def write(self, vals):
        res = True
        for rec in self:
            previous_member = rec.member_ids
            res = super(Project, rec).write(vals)
            after_member = rec.member_ids

            to_delete_members = previous_member - after_member
            if to_delete_members:
                rec.message_unsubscribe(partner_ids=to_delete_members.partner_id.ids)
            to_subscribe_members = after_member - previous_member
            if to_subscribe_members:
                rec.message_subscribe(partner_ids=to_subscribe_members.partner_id.ids)

        return res
