from odoo import models, fields, api
from datetime import timedelta


class ItemLine (models.Model):
    _name = 'scm.entry.item.line'
    _description = 'Item_line'

    name = fields.Char(string='Name', compute='_compute_name')
    item_id = fields.Many2one('ihh.package.item', string='Item', required=True)
    sequence = fields.Integer(string='Sequence', readonly=True, default=10)
    product_template_id = fields.Many2one(
        'product.template',
        related='item_id.product_template_id',
        string='POSM Template Item Name',
        store=True,
    )
    product_id = fields.Many2one(
        'product.product',
        string='POSM Item ID',
        readonly=True,
    )
    scm_id = fields.Many2one(
        'scm.entry',
        string='SCM Reference',
        readonly=True,
        ondelete='cascade',
        index=True,
    )
    allowed_channel_ids = fields.Many2many(
        'ihh.channel',
        string='Allowed Channel',
        related='scm_id.channel_ids',
    )
    allocated_item_ids = fields.Many2many(
        'ihh.package.item',
        string='Already used item',
        related='scm_id.allocated_item_ids',
    )
    scm_package_line_id = fields.Many2one('scm.entry.package.line')
    package_id = fields.Many2one(
        string='Package',
        readonly=True,
        store=True,
        related='item_id.package_id',
    )
    channel_id = fields.Many2one(
        string='Channel',
        readonly=True,
        store=True,
        related='item_id.package_id.channel_id',
    )
    item_date_from = fields.Date(
        string='Date From',
        compute='_compute_item_date_from',
        store=True,
        readonly=False,
        required=True,
    )
    item_date_to = fields.Date(
        string='Date To',
        compute='_compute_item_date_to',
        store=True,
        readonly=False,
        required=True,
    )
    dimension = fields.Char(string='Dimension')
    shipping_allocating = fields.Selection([
        ('shipping', 'Shipping'),
        ('allocating', 'Allocating'),
    ], string='Shipping / Allocating')
    quantity = fields.Integer(string='Quantity', compute='_compute_quantity')
    main_address_quantity = fields.Integer(
        string='Quantity',
        compute='_compute_quantity',
    )
    item_tags_ids = fields.Many2many('ihh.item.tag', string='Brand Name')
    item_tags_names = fields.Char(compute='_compute_item_tags_names')
    state = fields.Selection(
        related='scm_id.state',
        string='SCM Status',
        readonly=True,
        copy=False,
        store=True,
    )
    categ_id = fields.Many2one(
        string='POSM Item Category',
        related='product_id.categ_id',
    )
    package_name = fields.Char(
        string='Package Name',
        related='item_id.package_name',
    )
    material = fields.Char(string='Material', related='product_id.material')
    weight = fields.Char(string='Weight', related='product_id.weight')
    final_dimension = fields.Char(
        string='Final Dimension', related='product_id.final_dimension')
    open_dimension = fields.Char(
        string='Open Dimension', related='product_id.open_dimension')
    printing_method = fields.Char(
        string='Printing Method', related='product_id.printing_method')
    printing_color = fields.Char(
        string='Color', related='product_id.printing_color')
    surface_coating = fields.Char(
        string='Surface Coating', related='product_id.surface_coating')
    finishing = fields.Char(string='Finishing', related='product_id.finishing')
    packing_instruction = fields.Char(
        string='Packing Instruction', related='product_id.packing_instruction')
    uom_id = fields.Many2one(
        string='Units of Measure', related='product_id.uom_id')
    notes = fields.Text(
        string='Notes', related='product_template_id.ihh_notes')
    extra_instruction = fields.Text(string='Extra Instruction')
    uom_id = fields.Many2one(
        string='Units of Measure', related='product_id.uom_id')
    item_total = fields.Integer(
        string='Items per package (TBC)',
        related='item_id.package_id.item_total',
    )
    scm_package_name = fields.Char(
        string='SCM Package Name',
        related='scm_package_line_id.scm_package_name',
    )
    scm_package_id = fields.Char(
        string='SCM Package ID', related='scm_package_line_id.scm_package_id')
    final_delivery_address_id = fields.Many2one(
        string='Delivery Address',
        related='scm_package_line_id.delivery_address_id')
    delivery_address = fields.Char(
        string='Delivery Address - Full',
        related='scm_package_line_id.delivery_address_id.contact_address_complete',
    )
    delivery_date = fields.Date(
        string='Delivery Date', compute='_compute_delivery_date')
    shipping_date = fields.Date(
        string='Shipping Date', compute='_compute_shipping_date')
    date_from = fields.Date(
        string='Campaign Start', related='scm_id.date_from')
    date_to = fields.Date(string='Campaign End', related='scm_id.date_to')
    project_id = fields.Many2one(
        string='Project Name', related='scm_id.project_id')
    show_in_vc = fields.Boolean(
        related='item_id.product_template_id.show_in_vc', store=True)
    extra = fields.Text(string='Extra Info...')
    exposal_date = fields.Date(string='Exposal date')
    user_id = fields.Many2one(string='Owner', related='scm_id.user_id')
    user_project_id = fields.Many2one(
        string='Project Manager', related='scm_id.user_project_id')
    manufacturing_company_name = fields.Text(
        string='Manufacturing Company',
        related='scm_package_line_id.manufacturing_company_name',
    )
    manufacturer_location = fields.Many2one(
        string='Manufacturer location',
        related='scm_package_line_id.manufacturer_location',
    )
    active = fields.Boolean('Active', related='scm_id.active')

    @api.depends(
        'scm_package_line_id.total_quantity',
        'item_id.package_quantity',
    )
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = (rec.scm_package_line_id.total_quantity * rec.item_id.package_quantity)
            rec.main_address_quantity = (
                rec.scm_package_line_id.quantity * rec.item_id.package_quantity
            )

    @api.depends('item_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.item_id.product_template_id.name

    @api.depends('scm_id.date_from')
    def _compute_item_date_from(self):
        """
        Select SCM date_from for Item item_date_from
        """
        for rec in self:
            rec.item_date_from = rec.scm_id.date_from

    @api.depends('scm_id.date_to')
    def _compute_item_date_to(self):
        """
        Select SCM date_to for Item item_date_to
        """
        for rec in self:
            rec.item_date_to = rec.scm_id.date_to

    @api.depends('item_tags_ids.name')
    def _compute_item_tags_names(self):
        for rec in self:
            names = rec.item_tags_ids.mapped('name')
            names = [n for n in names if n]
            rec.item_tags_names = ','.join(names)

    @api.depends('scm_id.date_from')
    def _compute_delivery_date(self):
        """
        Delivery date function (15 days before SCM date_from)
        """
        for rec in self:
            rec.delivery_date = rec.scm_id.date_from - timedelta(days=15)

    @api.depends('scm_id.date_from')
    def _compute_shipping_date(self):
        """
        Delivery date function (3 days before SCM date_from)
        """
        for rec in self:
            rec.shipping_date = rec.scm_id.date_from - timedelta(days=3)

    def name_get(self):
        """
        Function to append Brand Name to item name in Visibility calendar
        """
        res = []
        for item in self:
            name_array = [item.item_id.name] + item.item_tags_ids.mapped(
                'name')
            name_array = [n for n in name_array if n]
            name = ' - '.join(name_array)
            res.append((item.id, name))
        return res

    @api.model
    def create(self, vals):
        """
        When creating item_id, automatically create a package_id if it
        doesn't exist
        """
        res = super(ItemLine, self).create(vals)

        res.create_package_if_not_exist()

        return res

    def write(self, vals):
        res = super(ItemLine, self).write(vals)

        self.create_package_if_not_exist()
        self.delete_package_if_not_exist()

        return res

    def unlink(self):
        """
        Delete package line when Item line is removed
        """
        scm_ids = self.scm_id.ids
        res = super(ItemLine, self).unlink()
        self.delete_package_unlink_if_not_exist(scm_ids)
        return res

    def create_package_if_not_exist(self):
        is_created = self.env.context.get('package_update')
        if is_created:
            return
        self = self.with_context({'package_update': True})
        for record in self:
            packages_line = record.scm_id.package_line_ids

            if record.package_id not in packages_line.package_id:
                package = self.env['scm.entry.package.line'].create({
                    'package_id': record.package_id.id,
                    'scm_id': record.scm_id.id,
                })
                record.scm_package_line_id = package.id
            else:
                p_line = packages_line.filtered(
                    lambda r: r.package_id == record.package_id)[0]
                record.scm_package_line_id = p_line.id

    def delete_package_if_not_exist(self):
        entry_line = self.env['scm.entry.item.line']
        for record in self:
            entry_line._delete_package_if_not_exist(record.scm_id.id)

    @api.model
    def delete_package_unlink_if_not_exist(self, scm_ids):
        entry_line = self.env['scm.entry.item.line']
        for scm_id in scm_ids:
            entry_line._delete_package_if_not_exist(scm_id)

    @api.model
    def _delete_package_if_not_exist(self, scm_id):
        scm = self.env['scm.entry'].browse(scm_id)
        packages_lines = scm.package_line_ids
        package_item_lines = scm.item_line_ids.mapped('package_id')

        for p in packages_lines:
            if p.package_id not in package_item_lines:
                p.unlink()
