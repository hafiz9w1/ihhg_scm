from odoo import models, fields, api
from datetime import datetime


class SelectionCriterium(models.Model):
    _name = "scm.entry.package.line"
    _description = "Package Lines"

    name = fields.Char(string='Name', compute="_compute_name")
    scm_id = fields.Many2one(comodel_name="scm.entry")
    package_id = fields.Many2one('ihh.package', string='Package')
    delivery_address_id = fields.Many2one(comodel_name="res.partner", domain="[('package_id', '=', package_id)]")
    quantity = fields.Integer(compute='_compute_quantity', store=True, readonly=False)
    total_quantity = fields.Integer(compute="_compute_total_quantity")
    backup_quantity = fields.Integer(compute="_compute_total_quantity")
    scm_entry_item_line_id = fields.One2many(comodel_name="scm.entry.item.line", inverse_name="scm_package_line_id", readonly=True)
    brand_id = fields.Many2one('ihh.item.tag', string='Brand Name')
    scm_package_name = fields.Char(compute="_compute_scm_package_name", string='SCM Package Name')
    scm_package_id = fields.Char(compute="_compute_scm_package_id", string='SCM Package ID')

    # TODO see if more complexe name need to be done
    @api.depends('package_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.package_id.name

    @api.depends('quantity', 'package_id.secondary_address_ids.backup_quantity')
    def _compute_total_quantity(self):
        for rec in self:
            backup_quantity = rec.package_id.secondary_address_ids.mapped('backup_quantity')
            rec.total_quantity = rec.quantity + sum(backup_quantity)
            rec.backup_quantity = sum(backup_quantity)

    @api.depends('scm_id.date_from', 'brand_id.name', 'package_id.name', 'package_id.naming_convention')
    def _compute_scm_package_name(self):
        for rec in self:
            name = rec.package_id.name
            brand = rec.brand_id.name
            package_name = rec.package_id.name
            month = rec.scm_id.date_from.strftime('%m')
            year = rec.scm_id.date_from.strftime('%y')
            day = rec.scm_id.date_from.strftime('%d')
            if rec.package_id.naming_convention == 'LW':
                name = f"【{brand}_{package_name}】{month}{year}_プロモーション②"
            if rec.package_id.naming_convention == 'DY':
                name = f"PM_{brand}_{month}{day}_{package_name}"
            if rec.package_id.naming_convention == 'SCMART':
                name = f"{int(month)}月{int(day)}日展開開始_{package_name}"

            rec.scm_package_name = name

    @api.depends('scm_id.date_from', 'scm_id.category_id.name', 'package_id.name')
    def _compute_scm_package_id(self):
        for rec in self:
            rec.scm_package_id = (rec.scm_id.date_from.strftime("%y") + rec.scm_id.date_from.strftime("%d") + rec.scm_id.date_from.strftime("%m") + str(rec.scm_id.category_id.name)[:1] + str(rec.package_id.name)).replace(' ', '')

    # Preset quantity from package_id.quantity
    @api.depends('package_id.quantity')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.package_id.quantity
