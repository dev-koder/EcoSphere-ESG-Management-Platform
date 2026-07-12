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

    _sql_constraints = [
        ('points_required_positive', 'CHECK(points_required >= 0)', 'Points required cannot be negative.'),
        ('stock_positive', 'CHECK(stock >= 0)', 'Reward stock cannot be negative.')
    ]
