from odoo import models, fields, api


class SelectionCriterium(models.Model):
    _name = "scm.entry.package.line"
    _description = "Package Lines"

    name = fields.Char(string='Name', compute="_compute_name")
    scm_id = fields.Many2one(comodel_name="scm.entry")
    package_id = fields.Many2one('ihh.package', string='Package', domain="[('delivery_address_ids', 'in', delivery_address_id)]")
    delivery_address_id = fields.Many2one(comodel_name="res.partner", domain="[('package_id', '=', package_id)]")
    quantity = fields.Float()
    scm_entry_item_line_id = fields.One2many(comodel_name="scm.entry.item.line", inverse_name="scm_package_line_id", readonly=True)

    # TODO see if more complexe name need to be done
    @api.depends('package_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.package_id.name
