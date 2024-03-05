from odoo import models, fields

class StockDock(models.Model):
    # Specify the model name
    _name = "stock.dock"
    # Describe the model
    _description = "Dock records"

    # Define a Char field for the dock name, which is required
    name = fields.Char(string="Name", required=True)
