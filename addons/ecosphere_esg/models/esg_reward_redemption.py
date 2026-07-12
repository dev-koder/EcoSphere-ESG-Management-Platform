from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EsgRewardRedemption(models.Model):
    _name = 'esg.reward.redemption'
    _description = 'ESG Reward Redemption'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    reward_id = fields.Many2one('esg.reward', string='Reward', required=True)
    points_deducted = fields.Integer(string='Points Deducted')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    status = fields.Selection([
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='confirmed')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            reward = self.env['esg.reward'].browse(vals.get('reward_id'))
            employee = self.env['hr.employee'].browse(vals.get('employee_id'))
            
            if reward.stock <= 0:
                raise ValidationError("This reward is out of stock.")
            
            if employee.esg_total_points < reward.points_required:
                raise ValidationError("Insufficient points to redeem this reward.")
                
            vals['points_deducted'] = reward.points_required
            
        redemptions = super().create(vals_list)
        
        for redemption in redemptions:
            redemption.reward_id.stock -= 1
            self.env['esg.points.ledger'].create({
                'employee_id': redemption.employee_id.id,
                'source': 'redemption',
                'points_delta': -redemption.points_deducted,
                'reference': '%s,%s' % ('esg.reward.redemption', redemption.id)
            })
            
        return redemptions
