from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')
    channel_id = fields.Many2many('ihh.channel', string='Channel')
    selection_criteria_id = fields.Many2many('selection.criteria', string='Selection Criteria')
    store_regulations_id = fields.Many2many('store.regulations', string='Store Regulations')
    scm_shipping_address = fields.Char(string='Shipping Address')
    represents = fields.Char(string='Represents')
    is_dc = fields.Boolean(string='Is DC')
    targets_represented = fields.Char(string='Targets Represented')
