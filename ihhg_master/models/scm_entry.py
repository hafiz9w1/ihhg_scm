from odoo import models, fields


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='SCM Name', tracking=True, required=True)
    project_id = fields.Many2one('project.project', string='Related Project', required=True, tracking=True)
    project_scm_id = fields.Char(string='Project ID', tracking=True)
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, tracking=True)
    user_project_id = fields.Many2one('res.users', string='Project Manager', tracking=True)
    channel_id = fields.Many2many('ihh.channel', string='Channel', tracking=True)
    package_id = fields.Many2many('ihh.package', string='Package', store=True, tracking=True, domain="[('channel_id', '=', channel_id)]")
    item_id = fields.Many2many('ihh.item', string='Item', store=True, tracking=True, domain="[('package_id', '=', package_id)]")
    category_id = fields.Many2one('ihh.category', string='Campaign Category', tracking=True)
    originating_regulation_id = fields.Many2one('store.regulation.entry', string='Originating Regulation', tracking=True)
    campaign_type_id = fields.Many2one('campaign.type', string='Campaign Type', tracking=True)
    date_from = fields.Datetime(string='Campaign Start', tracking=True)
    date_to = fields.Datetime(string='Campaign Stop', tracking=True)
