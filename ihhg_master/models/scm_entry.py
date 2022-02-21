from odoo import models, fields, api


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='SCM Name', tracking=True, required=True, states={'lock': [('readonly', True)]})
    project_id = fields.Many2one('project.project', string='Related Project', tracking=True, states={'lock': [('readonly', True)]})
    project_scm_id = fields.Char(string='Project ID', tracking=True, states={'lock': [('readonly', True)]})
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, required=True, tracking=True, states={'lock': [('readonly', True)]})
    user_project_id = fields.Many2one('res.users', string='Project Manager', tracking=True)
    channel_ids = fields.Many2many('ihh.channel', string='Channel', states={'lock': [('readonly', True)]})
    package_ids = fields.Many2many('ihh.package', string='Package', domain="[('channel_id', 'in', channel_ids)]", states={'lock': [('readonly', True)]})
    item_line_ids = fields.One2many('ihh.item.line', 'scm_id', string='Item', domain="[('package_id', 'in', package_ids)]", states={'lock': [('readonly', True)]}, copy=True, auto_join=True)
    channel_ids_total = fields.Integer(compute='_compute_channel_ids_total', string='Total Channel')
    package_ids_total = fields.Integer(compute='_compute_package_ids_total', string='Total Package')
    item_line_ids_total = fields.Integer(compute='_compute_item_line_ids_total', string='Total Item')
    category_id = fields.Many2one('ihh.category', string='Campaign Category', tracking=True, states={'lock': [('readonly', True)]})
    originating_regulation_id = fields.Many2one('store.regulation.entry', string='Originating Regulation', tracking=True)
    campaign_type_id = fields.Many2one('campaign.type', string='Campaign Type', tracking=True, states={'lock': [('readonly', True)]})
    date_from = fields.Datetime(string='Campaign Start', tracking=True, states={'lock': [('readonly', True)]})
    date_to = fields.Datetime(string='Campaign Stop', tracking=True, states={'lock': [('readonly', True)]})
    note = fields.Text(string='Extra note...')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('lock', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    # Count total number of Channel per SCM
    @api.depends('channel_ids')
    def _compute_channel_ids_total(self):
        for channel in self:
            channel.channel_ids_total = len(channel.channel_ids)

    # Count total number of Package per SCM
    @api.depends('package_ids')
    def _compute_package_ids_total(self):
        for package in self:
            package.package_ids_total = len(package.package_ids)

    # Count total number of items per SCM
    @api.depends('item_line_ids')
    def _compute_item_line_ids_total(self):
        for item in self:
            item.item_line_ids_total = len(item.item_line_ids)

    # Change SCM state to cancelled
    def action_scm_cancel(self):
        self.state = 'cancel'

    # Change SCM state to draft from cancelled
    def action_scm_draft(self):
        self.state = 'draft'

    # Lock SCM
    def action_scm_lock(self):
        self.state = 'lock'

    # Unlock SCM
    def action_scm_unlock(self):
        self.state = 'draft'
