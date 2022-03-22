from odoo import models, fields, api
from datetime import datetime


class SelectionCriterium(models.Model):
    _name = "scm.entry.package.line"
    _description = "Package Lines"

    name = fields.Char(string='Name', compute="_compute_name")
    scm_id = fields.Many2one(comodel_name="scm.entry")
    package_id = fields.Many2one('ihh.package', string='Package')
    package_name = fields.Char(string='Package Name', related="package_id.long_name")
    delivery_address_id = fields.Many2one(comodel_name="res.partner", domain="[('package_id', '=', package_id)]")
    quantity = fields.Integer(compute='_compute_quantity', store=True, readonly=False)
    total_quantity = fields.Integer(compute="_compute_total_quantity")
    backup_quantity = fields.Integer(compute="_compute_total_quantity")
    scm_entry_item_line_id = fields.One2many(comodel_name="scm.entry.item.line", inverse_name="scm_package_line_id", readonly=True)
    brand_id = fields.Many2one('ihh.item.tag', string='Brand Name')
    scm_package_name = fields.Char(compute="_compute_scm_package_name", string='SCM Package Name', store=True, readonly=False)
    scm_package_id = fields.Char(compute="_compute_scm_package_id", string='SCM Package ID', store=True, readonly=False)

    delivery_address = fields.Char(compute="_compute_delivery_address", string='Delivery Address - Full')
    item_date_from = fields.Date(string='Finally Modified Date', related='scm_entry_item_line_id.item_date_from')
    project_id = fields.Many2one(string='Project Name', related='scm_id.project_id')
    channel_id = fields.Many2one(string='Channel', related='package_id.channel_id')
    uom_id = fields.Many2one(string='Units of Measure', related='scm_entry_item_line_id.product_id.uom_id')
    delivery_date = fields.Date(string='Delivery Date', related='scm_entry_item_line_id.delivery_date')
    shipping_date = fields.Date(string='Shipping Date', related='scm_entry_item_line_id.shipping_date')
    date_from = fields.Date(string='Campaign Start', related='scm_id.date_from')
    date_to = fields.Date(string='Campaign End', related='scm_id.date_to')
    extra = fields.Text(string='Extra info...', related='scm_entry_item_line_id.extra')
    description = fields.Text(string='Description')
    vacant_instruction = fields.Text(string='Vacant Instruction')
    tbd = fields.Text(string='TBD')
    seihin_number = fields.Text(string='Seihin Number')
    seihin_name = fields.Text(string='Seihin Name')
    packing_size = fields.Text(string='Packing Size')
    packing_weight = fields.Text(string='Packing weight')
    manufacturing_company_name = fields.Text(string='Manufacturing Company Name')
    manufacturer_location = fields.Text(string='Manufacturer location')

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
                name = f"{int(month)}月{int(day)}日展開開始_{package_name}"

            rec.scm_package_name = name

    @api.depends('scm_id.date_from', 'scm_id.category_id.name', 'package_id.name')
    def _compute_scm_package_id(self):
        for rec in self:
            year = rec.scm_id.date_from.strftime("%y") if rec.scm_id.date_from else ""
            day = rec.scm_id.date_from.strftime("%d") if rec.scm_id.date_from else ""
            month = rec.scm_id.date_from.strftime("%m") if rec.scm_id.date_from else ""
            rec.scm_package_id = (year + day + month + str(rec.scm_id.category_id.name)[:1] + str(rec.package_id.name)).replace(' ', '')

    # Preset quantity from package_id.quantity
    @api.depends('package_id.quantity')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.package_id.quantity

    @api.depends('delivery_address_id.street', 'delivery_address_id.street2', 'delivery_address_id.city', 'delivery_address_id.state_id.name', 'delivery_address_id.country_id.name')
    def _compute_delivery_address(self):
        for rec in self:
            rec.delivery_address = f"{rec.delivery_address_id.street},{rec.delivery_address_id.street2},{rec.delivery_address_id.city},{rec.delivery_address_id.state_id.name},{rec.delivery_address_id.country_id.name}."
