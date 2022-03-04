from odoo import models, fields, api


class ItemLine (models.Model):
    _name = 'scm.entry.item.line'
    _description = 'Item_line'

    name = fields.Char(string='Name', compute="_compute_name")
    item_id = fields.Many2one('product.template', string='Item', required=True)
    sequence = fields.Integer(string='Sequence', readonly=True, default=10)
    product_id = fields.Many2one('product.product', string='POSM Item ID', readonly=True)
    scm_id = fields.Many2one('scm.entry', string='SCM Reference', readonly=True, ondelete='cascade', index=True)
    allowed_channel_ids = fields.Many2many('ihh.channel', string='Allowed Channel', related="scm_id.channel_ids")
    allocated_item_ids = fields.Many2many('product.template', string='Already used item', related="scm_id.allocated_item_ids")
    scm_package_line_id = fields.Many2one('scm.entry.package.line')
    package_id = fields.Many2one(string='Package', readonly=True, store=True, related='item_id.package_id')
    channel_id = fields.Many2one(string='Channel', readonly=True, store=True, related='item_id.package_id.channel_id')
    item_date_from = fields.Date(
        string='Date From', compute='_compute_item_date_from', store=True, readonly=False, required=True)
    item_date_to = fields.Date(
        string='Date To', compute='_compute_item_date_to', store=True, readonly=False, required=True)
    dimension = fields.Char(string='Dimension')
    shipping_allocating = fields.Selection([
        ('shipping', 'Shipping'),
        ('allocating', 'Allocating')
    ], string='Shipping / Allocating')
    product_uom_id = fields.Many2one('uom.uom', string='UoM')
    quantity = fields.Integer(string='Quantity', compute="_compute_quantity")
    item_tags_ids = fields.Many2many('ihh.item.tag', string='Brand Name')
    state = fields.Selection(related='scm_id.state', string='SCM Status', readonly=True, copy=False, store=True)

    @api.depends('scm_package_line_id.total_quantity', 'item_id.package_quantity')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.scm_package_line_id.total_quantity * rec.item_id.package_quantity

    # TODO: implement more complexe logic if needed
    @api.depends('item_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.item_id.name

    # Select SCM date_from for Item item_date_from
    @api.depends('scm_id.date_from')
    def _compute_item_date_from(self):
        for rec in self:
            rec.item_date_from = rec.scm_id.date_from

    # Select SCM date_to for Item item_date_to
    @api.depends('scm_id.date_to')
    def _compute_item_date_to(self):
        for rec in self:
            rec.item_date_to = rec.scm_id.date_to

    # Function to append Brand Name to item name in Visibility calendar
    def name_get(self):
        res = []
        for item in self:
            name_array = [item.item_id.name] + item.item_tags_ids.mapped('name')
            name = ' - '.join(name_array)
            res.append((item.id, name))
        return res

    # When creating item_id, automatically create a package_id if it doesn't exist
    @api.model
    def create(self, vals):
        res = super(ItemLine, self).create(vals)

        res.create_package_if_not_exist()

        return res

    def write(self, vals):
        res = super(ItemLine, self).write(vals)

        self.create_package_if_not_exist()
        self.delete_package_if_not_exist()

        return res

    # Delete package line when Item line is removed
    def unlink(self):
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
                p_line = packages_line.filtered(lambda r: r.package_id == record.package_id)[0]
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
