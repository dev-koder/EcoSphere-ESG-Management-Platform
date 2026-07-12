from odoo import models, fields

class EsgAudit(models.Model):
    _name = 'esg.audit'
    _description = 'ESG Audit'

    name = fields.Char(string='Audit Name', required=True)
    department_id = fields.Many2one('esg.department', string='Department')
    auditor_id = fields.Many2one('res.users', string='Auditor')
    audit_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')
    ], string='Audit Type', required=True)
    scheduled_date = fields.Date(string='Scheduled Date')
    completion_date = fields.Date(string='Completion Date')
    status = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='planned')
    findings_summary = fields.Text(string='Findings Summary')
