from odoo import models, fields


class Channel (models.Model):
    _name = 'ihh.channel'
    _description = 'Channel'

    name = fields.Char(string='Channel')
    owner = fields.Char(string='Owner')
