from odoo import models, fields, api
from datetime import datetime


class StockPickingBatch(models.Model):
    # Inherit the 'stock.picking.batch' model
    _inherit = "stock.picking.batch"

    # Define a Many2one field for the vehicle category
    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category", string="Vehicle Category"
    )

    # Define a Many2one field for the vehicle
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")

    # Define a Many2one field for the dock
    dock_id = fields.Many2one("stock.dock", string="Dock")

    # Define a Float field for weight, computed and readonly
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)

    # Define a Float field for volume, computed and readonly
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)

    # Add a date field with today's date as default value
    date = fields.Date(string="Today's Date", default=fields.Date.today())

    # Define a Float field for total weight, computed and readonly
    total_weight = fields.Float(
        string="Total Weight", compute="_compute_weight", store=True
    )

    # Define a Float field for total volume, computed and readonly
    total_volume = fields.Float(
        string="Total Volume", compute="_compute_volume", store=True
    )

    # Define fields for counts of transfers and move lines
    transfer_count = fields.Integer(
        string="Transfer Count",
        compute="_compute_transfer_count",
        readonly=True,
        store=True,
    )
    move_line_count = fields.Integer(
        string="Move Line Count",
        compute="_compute_move_line_count",
        readonly=True,
        store=True,
    )

    # Compute method to calculate the total volume of the batch
    @api.depends("picking_ids.volume", "vehicle_category_id.max_volume")
    def _compute_volume(self):
        for batch in self:
            total_volume = sum(picking.volume for picking in batch.picking_ids)
            batch.total_volume = total_volume
            if batch.vehicle_category_id:
                max_volume = batch.vehicle_category_id.max_volume
                batch.volume = total_volume / max_volume if max_volume else 0.0
            else:
                batch.volume = 0.0

    # Compute method to calculate the total weight of the batch
    @api.depends("picking_ids.weight", "vehicle_category_id.max_weight")
    def _compute_weight(self):
        for batch in self:
            total_weight = sum(picking.weight for picking in batch.picking_ids)
            batch.total_weight = total_weight
            if batch.vehicle_category_id:
                max_weight = batch.vehicle_category_id.max_weight
                batch.weight = total_weight / max_weight if max_weight else 0.0
            else:
                batch.weight = 0.0

    # Compute method to calculate the display name of the batch
    @api.depends("weight", "volume")
    def _compute_display_name(self):
        for batch in self:
            batch.display_name = f"{batch.name} ({batch.total_weight} kg, {batch.total_volume} m³)"

    # Compute method to calculate the number of transfers in the batch
    @api.depends("picking_ids")
    def _compute_transfer_count(self):
        for batch in self:
            batch.transfer_count = len(batch.picking_ids)

    # Compute method to calculate the number of move lines in the batc
    @api.depends("move_ids")
    def _compute_move_line_count(self):
        for batch in self:
            batch.move_line_count = len(batch.move_ids)
