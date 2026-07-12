from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EsgEmployeeParticipation(models.Model):
    _name = 'esg.employee.participation'
    _description = 'ESG Employee Participation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    activity_id = fields.Many2one('esg.csr.activity', string='CSR Activity', required=True)
    proof = fields.Binary(string='Proof Document')
    approval_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', default='pending', tracking=True)
    points_earned = fields.Integer(string='Points Earned', default=10)
    completion_date = fields.Date(string='Completion Date', default=fields.Date.context_today)

    @api.constrains('approval_status', 'proof')
    def _check_evidence_requirement(self):
        evidence_required = self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_evidence_required')
        for record in self:
            if record.approval_status == 'approved' and evidence_required and not record.proof:
                raise ValidationError("Proof of participation is required for approval based on company settings.")

    def action_approve(self):
        for record in self:
            record.approval_status = 'approved'
            # Create points ledger entry
            self.env['esg.points.ledger'].create({
                'employee_id': record.employee_id.id,
                'source': 'csr',
                'points_delta': record.points_earned,
                'reference': '%s,%s' % ('esg.employee.participation', record.id)
            })
            record.message_post(body="Participation approved. %s points awarded." % record.points_earned, subtype_xmlid='mail.mt_note')
            
    def action_reject(self):
        for record in self:
            record.approval_status = 'rejected'
            record.message_post(body="Participation rejected.", subtype_xmlid='mail.mt_note')
