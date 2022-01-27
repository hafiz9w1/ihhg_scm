from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    scm_entry_id = fields.Many2one('scm.entry', string='SCM')
    project_id = fields.Many2one('project.project', string='Originating Project')
    chain = fields.Char(string='Chain Code')
    posm_item_id = fields.Char(string='POSM Item ID')

    # Inherit name to change string name
    name = fields.Char(string='POSM Item Name')

    # Display Rule (commuputed field) = [POSM Item ID] ＋ POSM Item Name
    display_rule = fields.Char(string='Display Rule')

    material = fields.Char(string='Material')
    final_dimensions = fields.Float(string='Final Dimensions(mm)')
    open_dimensions = fields.Float(string='Open Dimensions(mm)')
    printing_method = fields.Char(string='Printing Method')
    surface_coating = fields.Char(string='Surface Coating')
    finishing = fields.Char(string='Finishing')
    printing_company = fields.Char(string='Printing Company')
    disposal_cycle = fields.Date(string='Disposal Cycle')
