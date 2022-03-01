
from odoo import models, fields


class CampaignType(models.Model):
    _name = "ihh.campaign.type"
    _description = "Campaign Type"

    name = fields.Char(string='Name')
