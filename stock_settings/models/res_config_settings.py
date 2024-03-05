from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Add a boolean field to enable installation of the Stock Transport Module
    module_stock_transport = fields.Boolean(string='Install Stock Transport Module')
