from odoo import models, fields, api


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='SCM Name', tracking=True, required=True, states={'lock': [('readonly', True)]})
    project_id = fields.Many2one('project.project', string='Related Project', tracking=True, states={'lock': [('readonly', True)]})
    project_scm_id = fields.Char(string='Project ID', tracking=True, states={'lock': [('readonly', True)]})
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, required=True, tracking=True, states={'lock': [('readonly', True)]})
    user_project_id = fields.Many2one('res.users', string='Project Manager', tracking=True, states={'lock': [('readonly', True)]})
    channel_ids = fields.Many2many('ihh.channel', string='Channel', states={'lock': [('readonly', True)]})
    item_line_ids = fields.One2many('scm.entry.item.line', 'scm_id', string='Items', states={'lock': [('readonly', True)]}, copy=True)
    package_line_ids = fields.One2many('scm.entry.package.line', 'scm_id', string='Packages', states={'lock': [('readonly', True)]}, copy=True)
    channel_ids_total = fields.Integer(compute='_compute_total', string='Total Channel')
    package_line_ids_total = fields.Integer(compute='_compute_total', string='Total Package')
    item_line_ids_total = fields.Integer(compute='_compute_total', string='Total Item')
    category_id = fields.Many2one('ihh.category', string='Campaign Category', tracking=True, states={'lock': [('readonly', True)]})
    campaign_type_id = fields.Many2one('ihh.campaign.type', string='Campaign Type', tracking=True, states={'lock': [('readonly', True)]})
    date_from = fields.Date(string='Campaign Start', tracking=True, states={'lock': [('readonly', True)]})
    date_to = fields.Date(string='Campaign Stop', tracking=True, states={'lock': [('readonly', True)]})
    note = fields.Text(string='Extra note...')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('lock', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    # Count total number of Channel per SCM
    @api.depends('channel_ids', 'package_line_ids', 'item_line_ids')
    def _compute_total(self):
        for rec in self:
            rec.channel_ids_total = len(rec.channel_ids)
            rec.package_line_ids_total = len(rec.package_line_ids)
            rec.item_line_ids_total = len(rec.item_line_ids)

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
