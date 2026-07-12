from odoo import models, fields

class EsgProductProfile(models.Model):
    _name = 'esg.product.profile'
    _description = 'ESG Product Profile'

    product_id = fields.Many2one('product.template', string='Product', required=True, unique=True)
    recyclable = fields.Boolean(string='Recyclable')
    sustainable_material = fields.Boolean(string='Sustainable Material')
    carbon_footprint_per_unit = fields.Float(string='Carbon Footprint per Unit')
    certification_ids = fields.Char(string='Certifications', help='Comma separated tags')
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('product_id_uniq', 'unique(product_id)', 'A product can only have one ESG profile.')
    ]
