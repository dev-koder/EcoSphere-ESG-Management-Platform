from odoo import models, fields

class EsgBadge(models.Model):
    _name = 'esg.badge'
    _description = 'ESG Badge'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    icon = fields.Char(string='Icon Class', default='fa-trophy', help='FontAwesome icon class')
    rule_type = fields.Selection([
        ('total_xp', 'Total XP'),
        ('challenges_completed', 'Challenges Completed'),
        ('csr_completed', 'CSR Activities Completed')
    ], string='Rule Type', required=True)
    threshold_value = fields.Integer(string='Threshold Value', required=True)
    active = fields.Boolean(string='Active', default=True)
