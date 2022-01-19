from odoo import models, fields


class Channel (models.Model):
    _name = 'channel'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Channel'

    channel = fields.Char(string='Channel')
    owner = fields.Char(string='Owner')
