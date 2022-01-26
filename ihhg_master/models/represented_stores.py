from odoo import models, fields


class RepresentedStores(models.Model):
    _name = "represented.stores"
    _description = "Represented Stores"

    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')
    number = fields.Float(string='Number')
    store_regulations_id = fields.Many2many('store.regulations', string='Store Regulations')
