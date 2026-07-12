from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    esg_total_xp = fields.Integer(string='Total XP', compute='_compute_esg_totals', store=True)
    esg_total_points = fields.Integer(string='Total Points', compute='_compute_esg_totals', store=True)
    esg_badge_ids = fields.Many2many('esg.badge', string='ESG Badges')
    
    esg_challenge_participation_ids = fields.One2many('esg.challenge.participation', 'employee_id', string='Challenge Participations')
    esg_points_ledger_ids = fields.One2many('esg.points.ledger', 'employee_id', string='Points Ledger')

    @api.depends('esg_challenge_participation_ids.xp_awarded', 'esg_points_ledger_ids.points_delta')
    def _compute_esg_totals(self):
        for employee in self:
            challenges = self.env['esg.challenge.participation'].search([('employee_id', '=', employee.id), ('approval_status', '=', 'approved')])
            employee.esg_total_xp = sum(challenges.mapped('xp_awarded'))
            
            ledgers = self.env['esg.points.ledger'].search([('employee_id', '=', employee.id)])
            employee.esg_total_points = sum(ledgers.mapped('points_delta'))

    def _check_badge_unlock(self, employee):
        if not self.env["ir.config_parameter"].sudo().get_param("ecosphere_esg.esg_badge_auto_award"):
            return
            
        for badge in self.env["esg.badge"].search([("active", "=", True)]):
            if badge in employee.esg_badge_ids:
                continue
                
            unlocked = False
            if badge.rule_type == "total_xp":
                unlocked = employee.esg_total_xp >= badge.threshold_value
            elif badge.rule_type == "challenges_completed":
                unlocked = self.env["esg.challenge.participation"].search_count([
                    ("employee_id", "=", employee.id), ("approval_status", "=", "approved")
                ]) >= badge.threshold_value
            elif badge.rule_type == "csr_completed":
                unlocked = self.env["esg.employee.participation"].search_count([
                    ("employee_id", "=", employee.id), ("approval_status", "=", "approved")
                ]) >= badge.threshold_value
                
            if unlocked:
                employee.esg_badge_ids = [(4, badge.id)]
                employee.message_post(body=f"🏅 Badge unlocked: {badge.name}!", subtype_xmlid='mail.mt_note')
