from odoo import models, fields

class EsgChallenge(models.Model):
    _name = 'esg.challenge'
    _description = 'ESG Challenge'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(string='Title', required=True)
    category_id = fields.Many2one('esg.category', string='Category', domain=[('category_type', '=', 'challenge')])
    description = fields.Text(string='Description')
    xp = fields.Integer(string='XP Award', required=True, default=50)
    difficulty = fields.Selection([
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], string='Difficulty', default='easy')
    evidence_required = fields.Boolean(string='Evidence Required', default=True)
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('under_review', 'Under Review'),
        ('completed', 'Completed'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)

    def action_activate(self):
        for record in self:
            record.status = 'active'
    
    def action_submit_review(self):
        for record in self:
            record.status = 'under_review'
            
    def action_complete(self):
        for record in self:
            record.status = 'completed'
            
    def action_archive(self):
        for record in self:
            record.status = 'archived'
