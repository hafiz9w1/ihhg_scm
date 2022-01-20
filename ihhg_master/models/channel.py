from odoo import models, fields


class Channel (models.Model):
    _name = 'ihh.channel'
    _inherit = 'mail.thread'
    _description = 'Channel'

    channel = fields.Char(string='Channel')
    owner = fields.Char(string='Owner')
