from odoo import models, fields, api

class EsgPolicyAcknowledgement(models.Model):
    _name = 'esg.policy.acknowledgement'
    _description = 'ESG Policy Acknowledgement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    policy_id = fields.Many2one('esg.policy', string='Policy', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    acknowledged_date = fields.Date(string='Acknowledged Date')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged')
    ], string='Status', default='pending', tracking=True)

    def action_acknowledge(self):
        for record in self:
            record.status = 'acknowledged'
            record.acknowledged_date = fields.Date.context_today(self)
            record.message_post(body="Policy acknowledged by employee.", subtype_xmlid='mail.mt_note')
