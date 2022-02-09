from odoo import models, fields


class Category (models.Model):
    _name = 'ihh.category'
    _description = 'Category'

    name = fields.Char(string='Category')
