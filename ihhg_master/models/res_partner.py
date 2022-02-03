from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cpid = fields.Datetime(string='CPID')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')
    delivery_type = fields.Char(string='Delivery Type')
    user_id = fields.Many2one('res.users', string='Contact Person', default=lambda self: self.env.user, tracking=True)
    post_number = fields.Char(string='Post Number')
    prefecture = fields.Char(string='Prefecture')
    territory_code = fields.Char(string='Territory Code')
    channel_id = fields.Many2many('ihh.channel', string='Channel')
    selection_criteria_id = fields.Many2many('selection.criteria', string='Selection Criteria')
    store_regulations_id = fields.Many2many('store.regulations', string='Store Regulations')
    scm_shipping_address = fields.Char(string='Shipping Address')
    is_dc = fields.Boolean(string='Is DC')
    is_represents = fields.Boolean(string='Is Representing')
    is_reserve = fields.Boolean(string='Is Reserve')
    targets_represented = fields.Char(string='Targets Represented')
