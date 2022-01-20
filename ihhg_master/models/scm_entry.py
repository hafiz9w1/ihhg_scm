from odoo import models, fields


class SCMEntry(models.Model):
    _name = "scm.entry"
    _description = "SCM Entry"

    channel = fields.Many2one('ihh.channel', string='Total Volume')
    originating_regulation = fields.Char(string='Originating Regulation')
    product_tmpl_id = fields.Many2one('product.template', string='Product Template')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')

    # 3.	In the Chart, the SCM has function MakeProduct. The function will create actual product from template and while doing so, assign name and numbers
