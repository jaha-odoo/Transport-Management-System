from odoo import models, fields, api
from datetime import datetime

class StockPickingBatch(models.Model):
    # Inherit the 'stock.picking.batch' model
    _inherit = "stock.picking.batch"

    # Define a Many2one field for the vehicle category
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category", string="Vehicle Category")
    
    # Define a Many2one field for the vehicle
    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle")
    
    # Define a Many2one field for the dock
    dock_id = fields.Many2one("stock.dock", string="Dock")
    
    # Define a Float field for weight, computed and readonly
    weight = fields.Float(string='Weight', compute='_compute_weight', readonly=True, store=True)
    
    # Define a Float field for volume, computed and readonly
    volume = fields.Float(string='Volume', compute='_compute_volume', readonly=True, store=True)
    
    # Define a Date field
    date = fields.Date(string='Date')
    
    # Define an Integer field for the day of the date, computed
    day_of_date = fields.Integer(string='Day of Date', compute='_compute_day_of_date', store=True)

    # Compute method to calculate the day of the date
    @api.depends('date')
    def _compute_day_of_date(self):
        for batch in self:
            if batch.date:
                batch.day_of_date = datetime.strptime(str(batch.date), '%Y-%m-%d').day

    # Compute method to calculate the total volume of the batch
    @api.depends('picking_ids.volume', 'vehicle_category_id.max_volume')
    def _compute_volume(self):
        for batch in self:
            total_volume = sum(picking.volume for picking in batch.picking_ids)
            if batch.vehicle_category_id:
                max_volume = batch.vehicle_category_id.max_volume
                batch.volume = total_volume / max_volume if max_volume else 0.0
            else:
                batch.volume = 0.0

    # Compute method to calculate the total weight of the batch
    @api.depends('picking_ids.weight', 'vehicle_category_id.max_weight')
    def _compute_weight(self):
        for batch in self:
            total_weight = sum(picking.weight for picking in batch.picking_ids)
            if batch.vehicle_category_id:
                max_weight = batch.vehicle_category_id.max_weight
                batch.weight = total_weight / max_weight if max_weight else 0.0
            else:
                batch.weight = 0.0
