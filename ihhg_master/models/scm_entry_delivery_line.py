from odoo import models, fields


class SelectionCriterium(models.Model):
    _name = 'scm.entry.delivery.line'
    _description = 'Delivery Lines'

    scm_id = fields.Many2one(
        comodel_name='scm.entry',
        string='SCM Reference',
        readonly=True,
        ondelete='cascade',
        index=True,
    )
    scm_entry_package_line_id = fields.Many2one(
        comodel_name='scm.entry.package.line',
        readonly=True,
    )
    scm_entry_item_line_ids = fields.One2many(
        string='Items',
        related='scm_entry_package_line_id.scm_entry_item_line_ids',
    )
    delivery_address_id = fields.Many2one(
        comodel_name='res.partner',
        readonly=True,
    )
    quantity = fields.Integer(readonly=True)
    package_id = fields.Many2one(
        string='Package',
        related='scm_entry_package_line_id.package_id',
    )
    delivery_address = fields.Char(
        related='delivery_address_id.contact_address_complete',
    )
    project_id = fields.Many2one(
        string='Project Name',
        related='scm_id.project_id',
    )
    channel_id = fields.Many2one(
        string='Channel',
        related='scm_entry_package_line_id.channel_id',
    )
    package_name = fields.Char(
        string='Package Name',
        related='scm_entry_package_line_id.package_id.long_name',
    )
    description = fields.Text(string='Description')
    vacant_instruction = fields.Text(string='Vacant Instruction')

    manufacturing_company_name = fields.Text(
        string='Manufacturing Company Name',
        related='scm_entry_package_line_id.manufacturing_company_name',
    )
    manufacturer_location = fields.Many2one(
        string='Manufacturer location',
        related='scm_entry_package_line_id.manufacturer_location',
    )
    package_size = fields.Text(
        string='Package Size',
        related='scm_entry_package_line_id.package_size',
    )
    package_weight = fields.Text(
        string='Package Weight',
        related='scm_entry_package_line_id.package_weight',
    )
