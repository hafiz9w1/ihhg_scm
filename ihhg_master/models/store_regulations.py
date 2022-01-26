from odoo import models, fields


class StoreRegulations(models.Model):
    _name = "store.regulations"
    _description = "Store Regulation Entry"

    package_name = fields.Char(string='Package Name')
    store_regulation_entry_id = fields.Many2many('store.regulation.entry', string='Store Regulation Entry')
