from odoo import models, fields

class EsgCategory(models.Model):
    _name = 'esg.category'
    _description = 'ESG Category'

    name = fields.Char(string='Name', required=True)
    category_type = fields.Selection([
        ('csr_activity', 'CSR Activity'),
        ('challenge', 'Challenge'),
        ('training', 'Training')
    ], string='Category Type', required=True)
    active = fields.Boolean(string='Active', default=True)
