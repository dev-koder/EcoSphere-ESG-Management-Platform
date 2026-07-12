from odoo import models, fields, api

class EsgEnvironmentalGoal(models.Model):
    _name = 'esg.environmental.goal'
    _description = 'ESG Environmental Goal'

    name = fields.Char(string='Name', required=True)
    department_id = fields.Many2one('esg.department', string='Department')
    metric = fields.Char(string='Metric', help='e.g. kg CO2e / employee')
    baseline_value = fields.Float(string='Baseline Value')
    target_value = fields.Float(string='Target Value')
    current_value = fields.Float(string='Current Value', compute='_compute_current_value', store=False)
    uom = fields.Char(string='Unit of Measure (UoM)')
    start_date = fields.Date(string='Start Date')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('achieved', 'Achieved'),
        ('missed', 'Missed')
    ], string='Status', compute='_compute_current_value', store=False)

    def _compute_current_value(self):
        for goal in self:
            if not goal.department_id or not goal.start_date or not goal.deadline:
                goal.current_value = 0.0
                goal.status = 'on_track'
                continue
            
            transactions = self.env['esg.carbon.transaction'].search([
                ('department_id', '=', goal.department_id.id),
                ('date', '>=', goal.start_date),
                ('date', '<=', goal.deadline),
                ('state', '=', 'confirmed')
            ])
            goal.current_value = sum(transactions.mapped('co2e_calculated'))

            if goal.current_value <= goal.target_value:
                if fields.Date.today() > goal.deadline:
                    goal.status = 'achieved'
                else:
                    goal.status = 'on_track'
            else:
                if fields.Date.today() > goal.deadline:
                    goal.status = 'missed'
                else:
                    goal.status = 'at_risk'
