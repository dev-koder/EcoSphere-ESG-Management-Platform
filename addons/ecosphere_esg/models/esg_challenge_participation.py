from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EsgChallengeParticipation(models.Model):
    _name = 'esg.challenge.participation'
    _description = 'ESG Challenge Participation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    challenge_id = fields.Many2one('esg.challenge', string='Challenge', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    progress = fields.Float(string='Progress (%)', default=0.0)
    proof = fields.Binary(string='Proof Document')
    approval_status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', default='pending', tracking=True)
    xp_awarded = fields.Integer(string='XP Awarded')

    @api.constrains('approval_status', 'proof')
    def _check_evidence_requirement(self):
        evidence_required = self.env['ir.config_parameter'].sudo().get_param('ecosphere_esg.esg_evidence_required')
        for record in self:
            if record.approval_status == 'approved' and (evidence_required or record.challenge_id.evidence_required) and not record.proof:
                raise ValidationError("Proof of participation is required for approval.")

    def action_approve(self):
        for record in self:
            record.approval_status = 'approved'
            record.progress = 100.0
            record.xp_awarded = record.challenge_id.xp
            
            # Create points ledger entry
            self.env['esg.points.ledger'].create({
                'employee_id': record.employee_id.id,
                'source': 'challenge',
                'points_delta': record.xp_awarded,
                'reference': '%s,%s' % ('esg.challenge.participation', record.id)
            })
            record.message_post(body="Challenge approved. %s XP awarded." % record.xp_awarded, subtype_xmlid='mail.mt_note')
            
            # Check badge unlock
            self.env['hr.employee']._check_badge_unlock(record.employee_id)
            
    def action_reject(self):
        for record in self:
            record.approval_status = 'rejected'
            record.message_post(body="Challenge participation rejected.", subtype_xmlid='mail.mt_note')
