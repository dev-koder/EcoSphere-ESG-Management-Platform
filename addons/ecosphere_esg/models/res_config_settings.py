from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    esg_auto_emission_calc = fields.Boolean(
        string='Auto Emission Calculation',
        config_parameter='ecosphere_esg.esg_auto_emission_calc'
    )
    esg_evidence_required = fields.Boolean(
        string='Evidence Required for CSR/Challenges',
        config_parameter='ecosphere_esg.esg_evidence_required'
    )
    esg_badge_auto_award = fields.Boolean(
        string='Badge Auto-Award',
        config_parameter='ecosphere_esg.esg_badge_auto_award'
    )
    esg_weight_environmental = fields.Integer(
        string='Environmental Weight (%)',
        default=40,
        config_parameter='ecosphere_esg.esg_weight_environmental'
    )
    esg_weight_social = fields.Integer(
        string='Social Weight (%)',
        default=30,
        config_parameter='ecosphere_esg.esg_weight_social'
    )
    esg_weight_governance = fields.Integer(
        string='Governance Weight (%)',
        default=30,
        config_parameter='ecosphere_esg.esg_weight_governance'
    )
