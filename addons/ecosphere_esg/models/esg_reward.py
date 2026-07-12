from odoo import models, fields

class EsgReward(models.Model):
    _name = 'esg.reward'
    _description = 'ESG Reward'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    points_required = fields.Integer(string='Points Required', required=True)
    stock = fields.Integer(string='Stock', required=True, default=10)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')
