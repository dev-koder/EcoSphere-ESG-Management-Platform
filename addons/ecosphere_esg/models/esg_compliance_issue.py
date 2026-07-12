from odoo import models, fields, api

class EsgComplianceIssue(models.Model):
    _name = 'esg.compliance.issue'
    _description = 'ESG Compliance Issue'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    audit_id = fields.Many2one('esg.audit', string='Audit')
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Severity', required=True)
    description = fields.Text(string='Description', required=True)
    owner_id = fields.Many2one('res.users', string='Owner', required=True, tracking=True)
    due_date = fields.Date(string='Due Date', required=True, tracking=True)
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], string='Status', default='open', tracking=True)
    
    is_overdue = fields.Boolean(string='Overdue', compute='_compute_is_overdue')

    @api.depends('due_date', 'status')
    def _compute_is_overdue(self):
        for issue in self:
            if issue.due_date and issue.status != 'resolved' and fields.Date.today() > issue.due_date:
                issue.is_overdue = True
            else:
                issue.is_overdue = False

    @api.model_create_multi
    def create(self, vals_list):
        issues = super().create(vals_list)
        for issue in issues:
            if issue.owner_id:
                issue.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=issue.owner_id.id,
                    date_deadline=issue.due_date,
                    summary='New Compliance Issue Assigned'
                )
        return issues
