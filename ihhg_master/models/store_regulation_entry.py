from odoo import models, fields


class StoreRegulationEntry(models.Model):
    _name = "store.regulation.entry"
    _description = "Store Regulation Entry"

    name = fields.Char(string='Name')
    product_tmpl_id = fields.Many2one('product.template', string='Product Template')
    placable_number = fields.Float(string='Placable Number')
