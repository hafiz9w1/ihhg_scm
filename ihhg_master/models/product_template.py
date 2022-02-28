from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    package_id = fields.Many2one('ihh.package', string='Package', readonly=True)
    channel_id = fields.Many2one('ihh.channel', string='Channel', related="package_id.channel_id", store=True)
    package_quantity = fields.Integer()

    chain = fields.Char(string='Chain Code')
    material = fields.Char(string='Material')
    final_dimensions = fields.Float(string='Final Dimensions(mm)')
    open_dimensions = fields.Float(string='Open Dimensions(mm)')
    printing_method = fields.Char(string='Printing Method')
    surface_coating = fields.Char(string='Surface Coating')
    finishing = fields.Char(string='Finishing')
    printing_company = fields.Char(string='Printing Company')
    disposal_cycle = fields.Date(string='Disposal Cycle')
