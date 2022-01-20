from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')
    channel_id = fields.Many2many('ihh.channel', string='Channel')
    selection_criteria_id = fields.Many2many('selection.criteria', string='Selection Criteria')
    store_regulation_entry_id = fields.Many2many('store.regulation.entry', string='Store Regulation')
    parent_address = fields.Char(string='Parent Address')
    is_dc = fields.Boolean(string='Is DC')
    targets_represented = fields.Char(string='Targets Represented')
