from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    # Define a field to store the total volume of the picking
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    # Define a field to store the total weight of the picking
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)

    # Compute method to calculate the total volume of the picking
    @api.depends("move_ids.product_id.volume", "move_ids.product_qty")
    def _compute_volume(self):
        for picking in self:
            # Calculate the total volume by summing the volume of each move
            volume = sum(
                move.product_id.volume * move.product_qty for move in picking.move_ids
            )
            # Update the volume field of the picking with the calculated value
            picking.volume = volume

    # Compute method to calculate the total weight of the picking
    @api.depends("move_ids.product_id.weight", "move_ids.product_qty")
    def _compute_weight(self):
        for picking in self:
            # Calculate the total weight by summing the weight of each move
            weight = sum(
                move.product_id.weight * move.product_qty for move in picking.move_ids
            )
            # Update the weight field of the picking with the calculated value
            picking.weight = weight
