from odoo import models, fields, api


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='SCM Name', tracking=True, required=True)
    project_id = fields.Many2one('project.project', string='Related Project', tracking=True)
    project_scm_id = fields.Char(string='Project ID', tracking=True)
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, required=True, tracking=True)
    user_project_id = fields.Many2one('res.users', string='Project Manager', tracking=True)
    channel_id = fields.Many2many('ihh.channel', string='Channel', tracking=True)
    package_id = fields.Many2many('ihh.package', string='Package', tracking=True, domain="[('channel_id', '=', channel_id)]")
    item_line_id = fields.Many2many('ihh.item.line', string='Item', tracking=True, domain="[('package_id', '=', package_id)]")
    channel_id_total = fields.Integer(compute='_compute_channel_id_total', string='Total Channel')
    package_id_total = fields.Integer(compute='_compute_package_id_total', string='Total Package')
    item_line_total = fields.Integer(compute='_compute_item_line_total', string='Total Item')
    category_id = fields.Many2one('ihh.category', string='Campaign Category', tracking=True)
    originating_regulation_id = fields.Many2one('store.regulation.entry', string='Originating Regulation', tracking=True)
    campaign_type_id = fields.Many2one('campaign.type', string='Campaign Type', tracking=True)
    date_from = fields.Datetime(string='Campaign Start', tracking=True)
    date_to = fields.Datetime(string='Campaign Stop', tracking=True)
    note = fields.Text(string='Extra note...')

    # Count total number of Channel per SCM
    @api.depends('channel_id')
    def _compute_channel_id_total(self):
        for channel in self:
            channel.channel_id_total = len(channel.channel_id)

    # Count total number of Package per SCM
    @api.depends('package_id')
    def _compute_package_id_total(self):
        for package in self:
            package.package_id_total = len(package.package_id)

    # Count total number of items per SCM
    @api.depends('item_line_id')
    def _compute_item_line_total(self):
        for item in self:
            item.item_line_total = len(item.item_line_id)
