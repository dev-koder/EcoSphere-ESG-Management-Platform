from odoo import models, fields

class EsgCsrActivity(models.Model):
    _name = 'esg.csr.activity'
    _description = 'ESG CSR Activity'

    title = fields.Char(string='Title', required=True)
    category_id = fields.Many2one('esg.category', string='Category', domain=[('category_type', 'in', ['csr_activity', 'training'])])
    organizing_department_id = fields.Many2one('esg.department', string='Organizing Department')
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    location = fields.Char(string='Location')
    max_participants = fields.Integer(string='Max Participants', default=0, help='0 = unlimited')
    status = fields.Selection([
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='planned')
