from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    posm_item_id = fields.Char(string='POSM Item ID')
    show_in_vc = fields.Boolean(string="Show in VC")
    dispose_after = fields.Integer(string="Dispose After (days)")

    extra_instruction = fields.Char(string='Extra Instruction')
    material = fields.Char(string='Material')
    weight = fields.Char(string='Weight')
    printing_medium = fields.Char(string='Printing Medium')
    packed_size = fields.Char(string='Packed size (mm)')
    display_size = fields.Char(string='Dispay size (mm)')
    printing_method = fields.Char(string='Printing Method')
    final_dimension = fields.Char(string='Final Dimensions(mm)')
    open_dimension = fields.Char(string='Open Dimensions(mm)')
    printing_color = fields.Char(string='Printing Colors')
    surface_coating = fields.Char(string='Surface Coating')
    finishing = fields.Char(string='Finishing')
    packing_instruction = fields.Char(string='Packing Instruction')
    description = fields.Char(string='Description')
    ihh_notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('posm_item_id_uniq', 'unique (posm_item_id)', "POSM Item ID already exists!"),
    ]
