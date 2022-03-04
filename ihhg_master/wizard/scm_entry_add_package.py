from odoo import models, fields, api


class ScmEntryAddPackage(models.TransientModel):
    _name = "scm.entry.add.package"
    _description = "Add Package to scm"

    scm_id = fields.Many2one(comodel_name="scm.entry")
    channel_ids = fields.Many2many(comodel_name="ihh.channel", related="scm_id.channel_ids")
    package_ids = fields.Many2many(comodel_name="ihh.package", domain="[('channel_id', 'in', channel_ids)]")

    @api.depends('scm_id.package_line_ids.package_id')
    def _compute_package_already_added(self):
        for rec in self:

            rec.package_already_added_ids = rec.scm_id.package_line_ids.package_id.ids

    def action_confirm(self):
        self.ensure_one()
        item_line_to_create = []
        for p in self.package_ids:
            if p not in self.scm_id.allocated_package_ids:
                package_line = self.env['scm.entry.package.line'].create({
                    'package_id': p.id,
                    'scm_id': self.scm_id.id,
                })
            else:
                package_line = self.scm_id.package_line_ids.filtered(lambda r: r.package_id == p)

            for item in p.item_ids:
                if item not in self.scm_id.allocated_item_ids:
                    item_line_to_create.append({
                        'item_id': item.id,
                        'scm_id': self.scm_id.id,
                        'scm_package_line_id': package_line.id,
                        'item_date_from': self.scm_id.date_from,
                        'item_date_to': self.scm_id.date_to
                    })
        self.env['scm.entry.item.line'].create(item_line_to_create)
