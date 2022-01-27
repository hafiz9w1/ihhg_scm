from odoo import models, fields


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    project_id = fields.Many2one('project.project', string='Related Project')
    project_scm_id = fields.Char(string='Project ID')
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, tracking=True)
    user_project_id = fields.Many2one('res.users', string='Project Manager', tracking=True)
    channel_id = fields.Many2one('ihh.channel', string='Channel')
    originating_regulation_id = fields.Many2one('store.regulation.entry', string='Originating Regulation')
    product_tmpl_id = fields.Many2one('product.template', string='Campaign Type')
    date_from = fields.Datetime(string='Campaign Start')
    date_to = fields.Datetime(string='Date To')

    # 3.	In the Chart, the SCM has function MakeProduct. The function will create actual product from template and while doing so, assign name and numbers
