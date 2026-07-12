from odoo import models, fields, api

class EsgDepartment(models.Model):
    _name = 'esg.department'
    _description = 'ESG Department'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    head_id = fields.Many2one('hr.employee', string='Department Head')
    parent_id = fields.Many2one('esg.department', string='Parent Department')
    employee_count = fields.Integer(string='Employee Count', compute='_compute_employee_count')
    status = fields.Selection([
        ('active', 'Active'),
        ('archived', 'Archived')
    ], string='Status', default='active')

    @api.depends('name') # In a real implementation this would depend on hr.employee
    def _compute_employee_count(self):
        for record in self:
            # Placeholder for actual employee count
            record.employee_count = self.env['hr.employee'].search_count([('department_id', '=', record.id)]) if 'department_id' in self.env['hr.employee']._fields else 0
