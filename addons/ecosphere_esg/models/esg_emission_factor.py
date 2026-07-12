from odoo import models, fields

class EsgEmissionFactor(models.Model):
    _name = 'esg.emission.factor'
    _description = 'ESG Emission Factor'

    name = fields.Char(string='Name', required=True)
    category = fields.Selection([
        ('fuel', 'Fuel'),
        ('electricity', 'Electricity'),
        ('purchase', 'Purchase'),
        ('travel', 'Travel'),
        ('waste', 'Waste'),
        ('other', 'Other')
    ], string='Category', required=True)
    scope = fields.Selection([
        ('1', 'Scope 1'),
        ('2', 'Scope 2'),
        ('3', 'Scope 3')
    ], string='Scope', required=True)
    uom = fields.Char(string='Unit of Measure (UoM)', help='e.g. liter, kWh, kg')
    co2e_per_unit = fields.Float(string='CO2e per Unit', required=True)
    source = fields.Char(string='Source', help='e.g. DEFRA 2024')
    active = fields.Boolean(string='Active', default=True)
