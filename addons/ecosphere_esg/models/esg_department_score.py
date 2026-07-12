from odoo import models, fields, api

class EsgDepartmentScore(models.Model):
    _name = 'esg.department.score'
    _description = 'ESG Department Score'

    department_id = fields.Many2one('esg.department', string='Department', required=True, unique=True)
    period_date = fields.Date(string='Last Recompute Date')
    environmental_score = fields.Float(string='Environmental Score', default=0.0)
    social_score = fields.Float(string='Social Score', default=0.0)
    governance_score = fields.Float(string='Governance Score', default=0.0)
    total_score = fields.Float(string='Total Score', default=0.0)

    _sql_constraints = [
        ('department_id_uniq', 'unique(department_id)', 'A department can only have one score record.')
    ]

    def _compute_environmental_score(self, department):
        goals = self.env['esg.environmental.goal'].search([('department_id', '=', department.id)])
        if not goals:
            return 100.0
        
        score_sum = 0
        for goal in goals:
            if goal.target_value == 0:
                score_sum += 100
                continue
            progress = (goal.current_value / goal.target_value) * 100
            # For carbon, lower is better. Assuming baseline > target.
            if goal.baseline_value > goal.target_value:
                expected_drop = goal.baseline_value - goal.target_value
                actual_drop = goal.baseline_value - goal.current_value
                prog = (actual_drop / expected_drop * 100) if expected_drop else 100
                score_sum += min(max(prog, 0), 100)
            else:
                score_sum += min(max(progress, 0), 100)
                
        return score_sum / len(goals)

    def _compute_social_score(self, department):
        employees = self.env['hr.employee'].search([('department_id', '=', department.id)])
        if not employees:
            return 100.0
            
        participations = self.env['esg.employee.participation'].search_count([
            ('employee_id', 'in', employees.ids),
            ('approval_status', '=', 'approved')
        ])
        challenges = self.env['esg.challenge.participation'].search_count([
            ('employee_id', 'in', employees.ids),
            ('approval_status', '=', 'approved')
        ])
        
        total_activities = participations + challenges
        expected_activities_per_emp = 5
        score = (total_activities / (len(employees) * expected_activities_per_emp)) * 100
        return min(score, 100.0)

    def _compute_governance_score(self, department):
        employees = self.env['hr.employee'].search([('department_id', '=', department.id)])
        open_issues = self.env['esg.compliance.issue'].search([
            ('audit_id.department_id', '=', department.id),
            ('status', '!=', 'resolved')
        ])
        
        severity_weights = {'low': 2, 'medium': 5, 'high': 15, 'critical': 30}
        issue_penalty = sum(severity_weights.get(issue.severity, 0) for issue in open_issues)
        
        required_policies = self.env['esg.policy'].search_count([('requires_acknowledgement', '=', True), ('status', '=', 'active')])
        ack_gap_penalty = 0
        if required_policies and employees:
            total_required_acks = required_policies * len(employees)
            actual_acks = self.env['esg.policy.acknowledgement'].search_count([
                ('employee_id', 'in', employees.ids),
                ('policy_id.requires_acknowledgement', '=', True),
                ('status', '=', 'acknowledged')
            ])
            ack_gap = total_required_acks - actual_acks
            ack_gap_penalty = (ack_gap / total_required_acks) * 20
            
        score = 100 - issue_penalty - ack_gap_penalty
        return max(score, 0.0)

    @api.model
    def recompute(self, department):
        if not department:
            return
            
        env_score = self._compute_environmental_score(department)
        soc_score = self._compute_social_score(department)
        gov_score = self._compute_governance_score(department)
        
        weights = {
            'env': int(self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_weight_environmental', '40') or '40'),
            'soc': int(self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_weight_social', '30') or '30'),
            'gov': int(self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_weight_governance', '30') or '30')
        }
        
        total = (env_score * weights['env'] + soc_score * weights['soc'] + gov_score * weights['gov']) / 100.0
        
        record = self.search([("department_id", "=", department.id)], limit=1)
        if not record:
            record = self.create({"department_id": department.id})
            
        record.write({
            "environmental_score": env_score,
            "social_score": soc_score,
            "governance_score": gov_score,
            "total_score": total,
            "period_date": fields.Date.today()
        })
        
    @api.model
    def get_dashboard_data(self):
        """RPC method for OWL dashboard"""
        departments = self.search([])
        scores = []
        for d in departments:
            scores.append({
                'department': d.department_id.name,
                'total_score': round(d.total_score, 1),
                'env_score': round(d.environmental_score, 1),
                'soc_score': round(d.social_score, 1),
                'gov_score': round(d.governance_score, 1),
            })
            
        # Top 10 Leaderboard
        employees = self.env['hr.employee'].search([], order='esg_total_xp desc', limit=10)
        leaderboard = []
        for e in employees:
            leaderboard.append({
                'name': e.name,
                'department': e.department_id.name if e.department_id else '',
                'xp': e.esg_total_xp,
                'points': e.esg_total_points
            })
            
        # Overall averages
        avg_env = sum(d['env_score'] for d in scores) / len(scores) if scores else 0
        avg_soc = sum(d['soc_score'] for d in scores) / len(scores) if scores else 0
        avg_gov = sum(d['gov_score'] for d in scores) / len(scores) if scores else 0
        
        weights = {
            'env': int(self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_weight_environmental', '40') or '40'),
            'soc': int(self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_weight_social', '30') or '30'),
            'gov': int(self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_weight_governance', '30') or '30')
        }
        overall = (avg_env * weights['env'] + avg_soc * weights['soc'] + avg_gov * weights['gov']) / 100.0
        
        # Carbon trend (mocked structure based on transactions)
        carbon_trend = {}
        transactions = self.env['esg.carbon.transaction'].read_group(
            domain=[('state', '=', 'confirmed')],
            fields=['date', 'co2e_calculated:sum'],
            groupby=['date:month']
        )
        for t in transactions:
            carbon_trend[t['date:month']] = t['co2e_calculated']
            
        return {
            'overall_score': round(overall, 1),
            'avg_env': round(avg_env, 1),
            'avg_soc': round(avg_soc, 1),
            'avg_gov': round(avg_gov, 1),
            'department_scores': scores,
            'leaderboard': leaderboard,
            'carbon_trend': carbon_trend
        }
