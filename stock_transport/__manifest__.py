{
    "name": "stock_transport",
    "author": "jatin",
    "depends": ["base", "fleet", "stock","stock_picking_batch"],
    "data": [
        "security/ir.model.access.csv",
        "views/vehicle_category_views.xml",
        "views/stock_picking_batch_views.xml",
        "views/stock_transfer_views.xml",
    ],
    "installable": True,
    "application": True,
}
