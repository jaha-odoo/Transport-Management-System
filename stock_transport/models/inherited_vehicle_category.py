from odoo import models, fields, api

class VehicleCategory(models.Model):
    # Inherit the 'fleet.vehicle.model.category' model
    _inherit = 'fleet.vehicle.model.category'

    # Define new fields for max weight and max volume
    max_weight = fields.Float(string='Max Weight (kg)')
    max_volume = fields.Float(string='Max Volume (m³)')

    # Compute method to update the display name based on the name, max weight, and max volume
    @api.depends('name', 'max_weight', 'max_volume')
    def _compute_display_name(self):
        # Iterate over each record (category) in the model
        for category in self:
            # Update the display_name field with a formatted string
            category.display_name = f"{category.name} ({category.max_weight}kg, {category.max_volume}m³)"
       
