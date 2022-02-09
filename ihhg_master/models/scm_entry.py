from odoo import models, fields, api


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
    package_id = fields.Many2many('ihh.package', string='Package', tracking=True)
    item_id = fields.Many2many('ihh.item', string='Item', tracking=True)
    category_id = fields.Many2one('ihh.category', string='Campaign Category', tracking=True)
    originating_regulation_id = fields.Many2one('store.regulation.entry', string='Originating Regulation', tracking=True)
    product_tmpl_id = fields.Many2one('product.template', string='Campaign Type', tracking=True)
    date_from = fields.Datetime(string='Campaign Start', tracking=True)
    date_to = fields.Datetime(string='Campaign Stop', tracking=True)
