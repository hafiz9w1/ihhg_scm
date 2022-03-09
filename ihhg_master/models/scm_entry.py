from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='SCM Name', tracking=True, required=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    project_id = fields.Many2one('project.project', string='Related Project', tracking=True, readonly=True)
    project_scm_id = fields.Char(string='Project ID', tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', string='Owner', default=lambda self: self.env.user, required=True, tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    user_project_id = fields.Many2one('res.users', string='Project Manager', tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    channel_ids = fields.Many2many('ihh.channel', string='Channel', states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    item_line_ids = fields.One2many('scm.entry.item.line', 'scm_id', string='Items', states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    allocated_item_ids = fields.Many2many(comodel_name="ihh.package.item", compute="_compute_allocated_item_ids")
    package_line_ids = fields.One2many('scm.entry.package.line', 'scm_id', string='Packages', states={'lock': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    allocated_package_ids = fields.Many2many(comodel_name="ihh.package", compute="_compute_allocated_package_ids")
    channel_ids_total = fields.Integer(compute='_compute_total', string='Total Channel')
    package_line_ids_total = fields.Integer(compute='_compute_total', string='Total Package')
    item_line_ids_total = fields.Integer(compute='_compute_total', string='Total Item')
    category_id = fields.Many2one('ihh.category', string='Campaign Category', tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    campaign_type_id = fields.Many2one('ihh.campaign.type', string='Campaign Type', tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    date_from = fields.Date(string='Campaign Start', tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    date_to = fields.Date(string='Campaign Stop', tracking=True, states={'lock': [('readonly', True)], 'phase2': [('readonly', True)], 'done': [('readonly', True)]})
    note = fields.Text(string='Extra note...')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('lock', 'Locked'),
        ('cancel', 'Cancelled'),
        ('phase2', 'Phase2'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    active = fields.Boolean('Active', default=True)

    # Count total number of Channel, Package and Item per SCM
    @api.depends('channel_ids', 'package_line_ids', 'item_line_ids')
    def _compute_total(self):
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

    # Change SCM state to cancelled
    def action_scm_cancel(self):
        self.state = 'cancel'

    # Change SCM state to draft from cancelled
    def action_scm_draft(self):
        self.state = 'draft'

    # Lock SCM
    def action_scm_lock(self):
        self.state = 'lock'

    # Unlock SCM
    def action_scm_unlock(self):
        self.state = 'draft'

    # Button for creating product.product from items and setting state to phase2
    def action_scm_confirm_items(self):
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
                    'printing_medium': line.item_id.product_template_id.printing_medium,
                    'packed_size': line.item_id.product_template_id.packed_size,
                    'display_size': line.item_id.product_template_id.display_size,
                    'printing_method': line.item_id.product_template_id.printing_method,
                    'printing_color': line.item_id.product_template_id.printing_color,
                    'surface_coating': line.item_id.product_template_id.surface_coating,
                    'finishing': line.item_id.product_template_id.finishing,
                    'packing_instruction': line.item_id.product_template_id.packing_instruction,
                    'ihh_notes': line.item_id.product_template_id.ihh_notes,
                })
                line.write({
                    "product_id": product.id
                })
        self.state = 'phase2'

    # Button for deleting product.product created by CONFRIM ITEM and setting state to lock
    def action_scm_reset(self):
        item_product_product = self.env['product.product'].search([('scm_id', 'in', self.ids)])
        item_product_product.unlink()

        self.state = 'lock'

    # Change state to done
    def action_scm_finish(self):
        self.state = 'done'

    # # Prevent SCM deletion in DONE state.
    # def unlink(self):
    #     for rec in self:
    #         if rec.state in ('done'):
    #             raise UserError(_('Deleting is not allowed for SCM in DONE state'))
    #     return super(SCMEntry, self).unlink()

    # # Prevent SCM duplication in DONE state.
    # def copy(self):
    #     for rec in self:
    #         if rec.state in ('done'):
    #             raise UserError(_('Duplication is not allowed for SCM in DONE state'))
    #     return super(SCMEntry, self).copy()

    def action_add_packages(self):
        self.ensure_one()
        add_package = self.env['scm.entry.add.package'].create({
            "scm_id": self.id
        })

        context = dict(self.env.context)

        return {
            'name': _('Add package'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'scm.entry.add.package',
            'res_id': add_package.id,
            'target': 'new',
            'context': context
        }
