from odoo import models, fields, api
from datetime import datetime


class SelectionCriterium(models.Model):
    _name = "scm.entry.delivery.line"
    _description = "Delivery Lines"

    scm_id = fields.Many2one(comodel_name="scm.entry")
    scm_entry_item_line_id = fields.Many2one(comodel_name="scm.entry.item.line", inverse_name="scm_package_line_id", readonly=True)
    delivery_address_id = fields.Many2one(comodel_name="res.partner", readonly=True)
    quantity = fields.Integer(readonly=True)
    package_id = fields.Many2one('ihh.package', string='Package', related='scm_entry_item_line_id.package_id')
    delivery_address = fields.Char(related="delivery_address_id.contact_address_complete")
    project_id = fields.Many2one(string='Project Name', related='scm_id.project_id')
    channel_id = fields.Many2one(string='Channel', related='scm_entry_item_line_id.channel_id')
    package_name = fields.Char(string='Package Name', related="package_id.long_name")
    extra = fields.Text(string='Extra info...', related='scm_entry_item_line_id.extra')
    description = fields.Text(string='Description')
    vacant_instruction = fields.Text(string='Vacant Instruction')
    uom_id = fields.Many2one(string='Units of Measure', related='scm_entry_item_line_id.uom_id')
    scm_package_name = fields.Char(string='SCM Package Name', related='scm_entry_item_line_id.scm_package_name')
    scm_package_id = fields.Char(string='SCM Package ID', related='scm_entry_item_line_id.scm_package_id')
    weight = fields.Char(string='Weight', related='scm_entry_item_line_id.weight')
    final_dimension = fields.Char(string='Final Dimension', related='scm_entry_item_line_id.final_dimension')
    manufacturing_company_name = fields.Text(string='Manufacturing Company Name')
    manufacturer_location = fields.Text(string='Manufacturer location')
    delivery_date = fields.Date(string='Delivery Date', related='scm_entry_item_line_id.delivery_date')
    shipping_date = fields.Date(string='Shipping Date', related='scm_entry_item_line_id.shipping_date')
    date_from = fields.Date(string='Campaign Start', related='scm_entry_item_line_id.date_from')
    date_to = fields.Date(string='Campaign End', related='scm_entry_item_line_id.date_to')
    final_modify_date = fields.Datetime(compute="_compute_final_modify_date")

    def _compute_final_modify_date(self):
        for rec in self:
            rec.final_modify_date = max(rec.scm_id.write_date, rec.scm_entry_item_line_id.write_date, rec.scm_entry_item_line_id.scm_package_line_id.write_date)
