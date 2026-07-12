from odoo import models, fields

class EsgPointsLedger(models.Model):
    _name = 'esg.points.ledger'
    _description = 'ESG Points Ledger'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    source = fields.Selection([
        ('challenge', 'Challenge'),
        ('csr', 'CSR Activity'),
        ('redemption', 'Reward Redemption'),
        ('manual', 'Manual Adjustment')
    ], string='Source', required=True)
    points_delta = fields.Integer(string='Points Delta', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    reference = fields.Reference([
        ('esg.challenge.participation', 'Challenge Participation'),
        ('esg.employee.participation', 'CSR Participation'),
        ('esg.reward.redemption', 'Reward Redemption')
    ], string='Reference')
