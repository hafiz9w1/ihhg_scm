from odoo import models, fields


class Channel (models.Model):
    _name = 'ihh.channel'
    _description = 'Channel'

    name = fields.Char(string='Channel')
    package_ids = fields.One2many(comodel_name="ihh.package", inverse_name="channel_id")
    active = fields.Boolean('Active', default=True)
