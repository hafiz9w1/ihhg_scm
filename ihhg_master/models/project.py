from datetime import timedelta, datetime
from odoo import models, fields, api, _


class Project(models.Model):
    _inherit = 'project.project'

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()

    scm_entry_id = fields.Many2one('scm.entry', string='SCM')

    # Add field in project to capture deadline (Delivery Date) for project
    project_date_deadline = fields.Datetime(string='Delivery Date', tracking=True)
    is_template = fields.Boolean(string='Is Template')

    # Project Team
    team_id = fields.Many2one(
        'crm.team', 'Project Team',
        ondelete="set null", tracking=True,
        change_default=True, default=_get_default_team
    )

    # Create new project based on project template
    @api.model
    def _map_project_tasks_default_values(self, task, project):
        """ get the default value for the copied task on project duplication """
        return {
            'stage_id': task.stage_id.id,
            'name': task.name,
            'project_offset': task.project_offset,
            'company_id': project.company_id.id,
        }

    def map_project_tasks(self, new_project_id):
        """ copy and map tasks from old to new project """
        project = self.browse(new_project_id)
        tasks = self.env['project.task']
        # We want to copy archived task, but do not propagate an active_test context key
        task_ids = self.env['project.task'].with_context(active_test=False).search([('project_id', '=', self.project_template.id)], order='parent_id').ids
        old_to_new_tasks = {}
        for task in self.env['project.task'].browse(task_ids):
            # preserve task name and stage, normally altered during copy
            defaults = self._map_project_tasks_default_values(task, project)
            if task.parent_id:
                # set the parent to the duplicated task
                defaults['parent_id'] = old_to_new_tasks.get(task.parent_id.id, False)
            new_task = task.copy(defaults)
            # If child are created before parent (ex sub_sub_tasks)
            new_child_ids = [old_to_new_tasks[child.id] for child in task.child_ids if child.id in old_to_new_tasks]
            tasks.browse(new_child_ids).write({'parent_id': new_task.id})
            old_to_new_tasks[task.id] = new_task.id
            tasks += new_task

        return project.write({'tasks': [(6, 0, tasks.ids)]})

    @api.returns('self', lambda value: value.id)
    def copy_project_as_template(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)") % (self.name)
        project = super(Project, self).copy(default)
        for follower in self.message_follower_ids:
            project.message_subscribe(partner_ids=follower.partner_id.ids, subtype_ids=follower.subtype_ids.ids)
        if 'tasks' not in default:
            self.map_project_tasks(project.id)
        return project


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
