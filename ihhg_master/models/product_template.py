from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    posm_item_id = fields.Char(string='POSM Item ID')
    show_in_vc = fields.Boolean(string="Show in VC")
    dispose_after = fields.Integer(string="Dispose After (days)")

    extra_instruction = fields.Char(string='Extra Instruction')
    material = fields.Char(string='Material')
    printing_medium = fields.Char(string='Printing Medium')
    packed_size = fields.Char(string='Packed size (mm)')
    display_size = fields.Char(string='Dispay size (mm)')
    printing_method = fields.Char(string='Printing Method')
    printing_color = fields.Char(string='Printing Colors')
    surface_coating = fields.Char(string='Surface Coating')
    finishing = fields.Char(string='Finishing')
    packing_instruction = fields.Char(string='Packing Instruction')
    ihh_notes = fields.Text(string='Notes')
