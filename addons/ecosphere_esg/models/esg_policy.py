from odoo import models, fields

class EsgPolicy(models.Model):
    _name = 'esg.policy'
    _description = 'ESG Policy'

    name = fields.Char(string='Name', required=True)
    policy_category = fields.Selection([
        ('governance', 'Governance'),
        ('environmental', 'Environmental'),
        ('social', 'Social')
    ], string='Policy Category', required=True)
    version = fields.Char(string='Version')
    document = fields.Binary(string='Document')
    effective_date = fields.Date(string='Effective Date')
    review_date = fields.Date(string='Next Review Date')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='draft')
    requires_acknowledgement = fields.Boolean(string='Requires Acknowledgement')
