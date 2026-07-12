from odoo import models, fields, api

class EsgCarbonTransaction(models.Model):
    _name = 'esg.carbon.transaction'
    _description = 'ESG Carbon Transaction'
    
    # ponytail: Manufacturing not wired into auto emission calc — same base_automation recipe as Purchase, add mrp.production trigger if time allows.

    department_id = fields.Many2one('esg.department', string='Department')
    source_module = fields.Selection([
        ('purchase', 'Purchase'),
        ('expense', 'Expense'),
        ('fleet', 'Fleet'),
        ('manual', 'Manual')
    ], string='Source Module', required=True, default='manual')
    
    source_reference = fields.Reference([
        ('purchase.order.line', 'Purchase Order Line'),
        ('hr.expense', 'Expense'),
        ('fleet.vehicle.log.fuel', 'Fleet Fuel Log')
    ], string='Source Reference')

    emission_factor_id = fields.Many2one('esg.emission.factor', string='Emission Factor', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    co2e_calculated = fields.Float(string='CO2e Calculated', compute='_compute_co2e_calculated', store=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], string='Status', default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.department_id:
                self.env['esg.department.score'].recompute(record.department_id)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.department_id:
                self.env['esg.department.score'].recompute(record.department_id)
        return res

    @api.depends('quantity', 'emission_factor_id.co2e_per_unit')
    def _compute_co2e_calculated(self):
        for record in self:
            if record.emission_factor_id:
                record.co2e_calculated = record.quantity * record.emission_factor_id.co2e_per_unit
            else:
                record.co2e_calculated = 0.0
