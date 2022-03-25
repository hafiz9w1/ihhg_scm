from odoo import models, fields, api
from datetime import datetime


class SelectionCriterium(models.Model):
    _name = "scm.entry.package.line"
    _description = "Package Lines"

    name = fields.Char(string='Name', compute="_compute_name")
    scm_id = fields.Many2one(comodel_name="scm.entry")
    package_id = fields.Many2one('ihh.package', string='Package')
    package_name = fields.Char(string='Package Name', related="package_id.long_name")
    delivery_address_id = fields.Many2one(comodel_name="res.partner", domain="[('package_ids', 'in', package_id)]")
    quantity = fields.Integer(compute='_compute_quantity', store=True, readonly=False)
    total_quantity = fields.Integer(compute="_compute_total_quantity")
    backup_quantity = fields.Integer(compute="_compute_total_quantity")
    scm_entry_item_line_ids = fields.One2many(comodel_name="scm.entry.item.line", inverse_name="scm_package_line_id", readonly=True)
    brand_id = fields.Many2one('ihh.item.tag', string='Brand Name', inverse="_inverse_add_brand_to_items")
    scm_package_name = fields.Char(compute="_compute_scm_package_name", string='SCM Package Name', store=True, readonly=False)
    scm_package_id = fields.Char(compute="_compute_scm_package_id", string='SCM Package ID', store=True, readonly=False)

    manufacturing_company_name = fields.Text(string='Manufacturing Company')
    manufacturer_location = fields.Many2one('res.partner', string='Manufacturer location')
    package_size = fields.Text(string='Package Size')
    package_weight = fields.Text(string='Package Weight')
    state = fields.Selection(string='State', related="scm_id.state")

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
            brand = rec.brand_id.name
            package_name = rec.package_id.long_name
            month = rec.scm_id.date_from.strftime('%m') if rec.scm_id.date_from else ""
            year = rec.scm_id.date_from.strftime('%y') if rec.scm_id.date_from else ""
            day = rec.scm_id.date_from.strftime('%d') if rec.scm_id.date_from else ""
            name = f"{year}{month}_{brand}_{package_name}"
            if rec.package_id.naming_convention == 'LW':
                name = f"【{brand}_{package_name}】{month}{year}_プロモーション②"
            if rec.package_id.naming_convention == 'DY':
                name = f"PM_{brand}_{month}{day}_{package_name}"
            if rec.package_id.naming_convention == 'SCMART':
                name = f"{month}月{day}日展開開始_{package_name}"

            rec.scm_package_name = name

    @api.depends('scm_id.date_from', 'scm_id.category_id.name', 'package_id.name')
    def _compute_scm_package_id(self):
        for rec in self:
            year = rec.scm_id.date_from.strftime("%y") if rec.scm_id.date_from else ""
            day = rec.scm_id.date_from.strftime("%d") if rec.scm_id.date_from else ""
            month = rec.scm_id.date_from.strftime("%m") if rec.scm_id.date_from else ""
            rec.scm_package_id = (year + month + day + str(rec.scm_id.category_id.name)[:1] + str(rec.package_id.name)).replace(' ', '')

    # Preset quantity from package_id.quantity
    @api.depends('package_id.quantity')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.package_id.quantity

    def _inverse_add_brand_to_items(self):
        for rec in self:
            rec.scm_entry_item_line_ids.write({
                "item_tags_ids": [(6, 0, rec.brand_id.ids)]
            })
