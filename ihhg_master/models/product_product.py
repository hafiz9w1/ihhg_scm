from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # remove computation, we are not use variant normally use
    # it to put a value linked to SCM
    combination_indices = fields.Char(compute=False)
    posm_item_id = fields.Char(string='POSM Item ID')
    scm_id = fields.Many2one(comodel_name='scm.entry', readonly=True)
    project_id = fields.Many2one(
        comodel_name='project.project',
        related='scm_id.project_id',
        store=True,
    )

    # Use to store the value for prdocut
    extra_instruction = fields.Char(string='Extra Instruction')
    material = fields.Char(string='Material')
    weight = fields.Char(string='Weight')
    printing_medium = fields.Char(string='Printing Medium')
    packed_size = fields.Char(string='Packed size (mm)')
    display_size = fields.Char(string='Dispay size (mm)')
    printing_method = fields.Char(string='Printing Method')
    final_dimension = fields.Char(string='Final Dimensions(mm)')
    open_dimension = fields.Char(string='Open Dimensions(mm)')
    surface_coating = fields.Char(string='Surface Coating')
    printing_color = fields.Char(string='Color')
    finishing = fields.Char(string='Finishing')
    packing_instruction = fields.Char(string='Packing Instruction')
    description = fields.Char(string='Description')
    ihh_notes = fields.Text(string='Notes')
    disposal_date = fields.Date()

    def name_get(self):
        names = []
        for rec in self:
            names.append((
                rec.id, f'[{rec.posm_item_id}-{rec.scm_id.name}] {rec.name}',
            ))

        return names
