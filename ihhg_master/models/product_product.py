from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    package_quantity = fields.Float()
    posm_item_id = fields.Char(string='POSM Item ID')
    scm_id = fields.Many2one(comodel_name="scm.entry", readonly=True)
    project_id = fields.Many2one(comodel_name="project.project", related="scm_id.project_id")
    chain = fields.Char(string='Chain Code')
    material = fields.Char(string='Material')
    final_dimensions = fields.Float(string='Final Dimensions(mm)')
    open_dimensions = fields.Float(string='Open Dimensions(mm)')
    printing_method = fields.Char(string='Printing Method')
    surface_coating = fields.Char(string='Surface Coating')
    finishing = fields.Char(string='Finishing')
    printing_company = fields.Char(string='Printing Company')
    disposal_cycle = fields.Date(string='Disposal Cycle')
