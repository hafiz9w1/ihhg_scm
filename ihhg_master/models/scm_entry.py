from datetime import timedelta
import json
from odoo import models, fields, api, _
from urllib.parse import urlencode


class SCMEntry(models.Model):
    _name = 'scm.entry'
    _description = 'SCM Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='SCM Name',
        tracking=True,
        required=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    project_id = fields.Many2one(
        'project.project',
        string='Related Project',
        tracking=True,
        readonly=True,
        copy=False,
    )
    project_scm_id = fields.Char(
        string='Project ID',
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    user_id = fields.Many2one(
        'res.users',
        string='Owner',
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    user_budget_id = fields.Many2one(
        'res.users',
        string='Budget Owner',
        default=lambda self: self.env.user.has_group(
            'ihhg_master.group_scm_cp_team'),
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    user_project_id = fields.Many2one(
        'res.users',
        string='Project Manager',
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    channel_ids = fields.Many2many(
        'ihh.channel',
        string='Channel',
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    item_line_ids = fields.One2many(
        'scm.entry.item.line',
        'scm_id', string='Items',
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
        copy=True,
    )
    item_line_ids_mass_production = fields.One2many(
        string='Items Mass Production',
        related='item_line_ids',
    )
    item_line_ids_adaption_work = fields.One2many(
        string='Items Adaption Work',
        related='item_line_ids',
    )
    package_line_ids_delivery = fields.One2many(
        comodel_name='scm.entry.delivery.line',
        inverse_name='scm_id',
        string='Items Delivery',
        readonly=True,
    )
    allocated_item_ids = fields.Many2many(
        comodel_name='ihh.package.item',
        compute='_compute_allocated_item_ids',
    )
    package_line_ids = fields.One2many(
        'scm.entry.package.line',
        'scm_id', string='Packages',
        states={
            'lock': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
        copy=False,
    )
    allocated_package_ids = fields.Many2many(
        comodel_name='ihh.package',
        compute='_compute_allocated_package_ids',
    )
    channel_ids_total = fields.Integer(
        compute='_compute_total',
        string='Total Channel',
    )
    package_line_ids_total = fields.Integer(
        compute='_compute_total',
        string='Total Package',
    )
    item_line_ids_total = fields.Integer(
        compute='_compute_total',
        string='Total Item',
    )
    category_id = fields.Many2one(
        'ihh.category',
        string='Campaign Category',
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    date_from = fields.Date(
        string='Campaign Start',
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    date_to = fields.Date(
        string='Campaign Stop',
        tracking=True,
        states={
            'lock': [('readonly', True)],
            'phase2': [('readonly', True)],
            'done': [('readonly', True)],
            'cancel': [('readonly', True)]},
    )
    note = fields.Text(string='Extra note...')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('lock', 'Locked'),
        ('cancel', 'Cancelled'),
        ('phase2', 'Item Confirmed'),
        ('done', 'Done'),
    ],string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    active = fields.Boolean('Active', default=True)

    @api.depends('channel_ids', 'package_line_ids', 'item_line_ids')
    def _compute_total(self):
        """
        Count total number of Channel, Package and Item per SCM
        """
        for rec in self:
            rec.channel_ids_total = len(rec.channel_ids)
            rec.package_line_ids_total = len(rec.package_line_ids)
            rec.item_line_ids_total = len(rec.item_line_ids)

    @api.depends('item_line_ids.item_id')
    def _compute_allocated_item_ids(self):
        for rec in self:
            rec.allocated_item_ids = rec.item_line_ids.item_id.ids

    @api.depends('package_line_ids.package_id')
    def _compute_allocated_package_ids(self):
        for rec in self:
            rec.allocated_package_ids = rec.package_line_ids.package_id.ids

    def action_scm_cancel(self):
        """
        Change SCM state to cancelled
        """
        self.state = 'cancel'

    def action_scm_draft(self):
        """
        Change SCM state to draft from cancelled
        """
        self.state = 'draft'

    def action_scm_lock(self):
        """
        Lock SCM
        """
        self.state = 'lock'

    def action_scm_unlock(self):
        """
        Unlock SCM
        """
        self.state = 'draft'

    def action_scm_confirm_items(self):
        """
        Button for creating product.product from items and
        setting state to phase2
        """
        for rec in self:
            for line in rec.item_line_ids:
                product = self.env['product.product'].create({
                    'posm_item_id': line.name,
                    'product_tmpl_id': line.item_id.product_template_id.id,
                    'combination_indices': f"{str(rec.id)}-{str(line.package_id.id)}",
                    'scm_id': rec.id,
                    # copy value from template
                    'extra_instruction': line.item_id.product_template_id.extra_instruction,
                    'material': line.item_id.product_template_id.material,
                    'weight': line.item_id.product_template_id.weight,
                    'printing_medium': line.item_id.product_template_id.printing_medium,
                    'packed_size': line.item_id.product_template_id.packed_size,
                    'display_size': line.item_id.product_template_id.display_size,
                    'printing_method': line.item_id.product_template_id.printing_method,
                    'final_dimension': line.item_id.product_template_id.final_dimension,
                    'open_dimension': line.item_id.product_template_id.open_dimension,
                    'surface_coating': line.item_id.product_template_id.surface_coating,
                    'printing_color': line.item_id.product_template_id.printing_color,
                    'finishing': line.item_id.product_template_id.finishing,
                    'packing_instruction': line.item_id.product_template_id.packing_instruction,
                    'description': line.item_id.product_template_id.description,
                    'ihh_notes': line.item_id.product_template_id.ihh_notes,
                    'disposal_date': rec.date_to + timedelta(days=line.item_id.product_template_id.dispose_after),
                })
                line.write({
                    "product_id": product.id,
                })
            for address in rec.package_line_ids:
                address.create_delivery_line()
        self.state = 'phase2'

    def action_scm_reset(self):
        """
        Button for deleting product.product created by CONFRIM ITEM and
        setting state to lock
        """
        item_product_product = self.env['product.product'].search(
            [('scm_id', 'in', self.ids)])
        item_product_product.unlink()
        self.write({'package_line_ids_delivery': [(
            5, 0, 0)]})

        self.state = 'lock'

    def action_scm_finish(self):
        """
        Change state to done
        """
        self.state = 'done'

    def action_add_packages(self):
        self.ensure_one()
        add_package = self.env['scm.entry.add.package'].create({
            'scm_id': self.id,
        })
        context = dict(self.env.context)
        return {
            'name': _('Add package'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'scm.entry.add.package',
            'res_id': add_package.id,
            'target': 'new',
            'context': context,
        }

    def action_mass_production_download(self):
        """
        Download Mass Production to excel
        """
        data = {
            "data": json.dumps({
                "model": 'scm.entry.item.line',
                "fields": [
                    {"name": "item_date_from", "label": _("Date")},
                    {"name": "project_id", "label": _("Project Name")},
                    {"name": "channel_id", "label": _("Channel")},
                    {"name": "categ_id", "label": _("POSM Item Category")},
                    {"name": "package_id", "label": _("Packing ID")},
                    {"name": "package_name", "label": _("Package Name")},
                    {"name": "item_id", "label": _("POSM Item ID")},
                    {"name": "name", "label": _("POSM Item Name")},
                    {"name": "item_tags_names", "label": _("Brand Name")},
                    {"name": "material", "label": _("Material")},
                    {"name": "weight", "label": _("Weight")},
                    {"name": "final_dimension", "label": _("Final Dimenions")},
                    {"name": "open_dimension", "label": _("Open Dimension")},
                    {"name": "printing_method", "label": _("Printing Method")},
                    {"name": "printing_color", "label": _("Color")},
                    {"name": "surface_coating", "label": _("Surface Coating")},
                    {"name": "finishing", "label": _("Finishing")},
                    {"name": "packing_instruction", "label": _("Packing Instruction")},
                    {"name": "notes", "label": _("Notes")},
                    {"name": "extra_instruction", "label": _("Extra Instruction")},
                    {"name": "quantity", "label": _("Quantity")},
                    {"name": "uom_id", "label": _("Units of Measure")},
                    {"name": "item_total", "label": _("Items per package (TBC)")},
                    {"name": "scm_package_id", "label": _("SCM Package ID")},
                    {"name": "scm_package_name", "label": _("SCM Package Name")},
                    {"name": "final_delivery_address_id", "label": _("Delivery Address")},
                    {"name": "delivery_address", "label": _("Delivery Address - Full")},
                    {"name": "delivery_date", "label": _("Delivery Date")},
                    {"name": "shipping_date", "label": _("Shipping Date")},
                    {"name": "date_from", "label": _("Campaign Start")},
                    {"name": "date_to", "label": _("Campaign End")},
                    {"name": "extra", "label": _("Extra Info...")},
                    {"name": "exposal_date", "label": _("Exposal Date")},
                    {"name": "user_id", "label": _("Owner")},
                    {"name": "user_project_id", "label": _("Project Manager")},
                    {"name": "manufacturing_company_name", "label": _("Manufacturing Company")},
                    {"name": "manufacturer_location", "label": _("Manufacturer location")},
                ],
                "ids": self.item_line_ids_mass_production.ids,
                "domain": [],
                "import_compat": False
            })
        }
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/export/xlsx?{urlencode(data)}',
            'target': 'self',
        }

    def action_adaption_work_download(self):
        """
        Download Adaption Work to excel
        """
        data = {
            "data": json.dumps({
                "model": 'scm.entry.item.line',
                "fields": [
                    {"name": "item_date_from", "label": _("Date")},
                    {"name": "project_id", "label": _("Project Name")},
                    {"name": "channel_id", "label": _("Channel")},
                    {"name": "item_id", "label": _("POSM Item ID")},
                    {"name": "name", "label": _("POSM Item Name")},
                    {"name": "item_tags_names", "label": _("Brand Name")},
                    {"name": "material", "label": _("Material")},
                    {"name": "weight", "label": _("Weight")},
                    {"name": "final_dimension", "label": _("Final Dimenions")},
                    {"name": "open_dimension", "label": _("Open Dimension")},
                    {"name": "printing_method", "label": _("Printing Method")},
                    {"name": "printing_color", "label": _("Color")},
                    {"name": "surface_coating", "label": _("Surface Coating")},
                    {"name": "finishing", "label": _("Finishing")},
                    {"name": "manufacturing_company_name", "label": _("Manufacturing Company")},
                    {"name": "manufacturer_location", "label": _("Manufacturer location")},
                    {"name": "date_from", "label": _("Campaign Start")},
                    {"name": "date_to", "label": _("Campaign End")},
                    {"name": "notes", "label": _("Notes")},
                    {"name": "extra_instruction", "label": _("Extra Instruction")},
                ],
                "ids": self.item_line_ids_adaption_work.ids,
                "domain": [],
                "import_compat": False
            })
        }
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/export/xlsx?{urlencode(data)}',
            'target': 'self',
        }

    def action_delivery_download(self):
        """
        Download Delivery to excel
        """
        data = {
            'data': json.dumps({
                'model': 'scm.entry.delivery.line',
                "fields": [
                    {'name': "delivery_address_id", "label": _("Delivery Address")},
                    {"name": "delivery_address", "label": _("Delivery Address - Full")},
                    {"name": "project_id", "label": _("Project Name")},
                    {"name": "channel_id", "label": _("Channel")},
                    {"name": "package_id", "label": _("Packing ID")},
                    {"name": "package_name", "label": _("Package Name")},
                    {"name": "description", "label": _("Description")},
                    {"name": "vacant_instruction", "label": _("Vacant Instruction")},
                    {"name": "quantity", "label": _("Quantity")},
                    {"name": "manufacturing_company_name", "label": _("Manufacturing Company Name")},
                    {"name": "manufacturer_location", "label": _("Manufacturer location")},
                    {"name": "scm_entry_item_line_ids", "label": _("Items")},
                ],
                "ids": self.package_line_ids_delivery.ids,
                "domain": [],
                "import_compat": False
            })
        }
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/export/xlsx?{urlencode(data)}',
            'target': 'self',
        }
