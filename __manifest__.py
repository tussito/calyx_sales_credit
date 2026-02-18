{
    "name": "Calyx - Canales de Venta y Control de Crédito",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "summary": "Canales (depósito/diario) + grupos de crédito + bloqueo + reporte + endpoint",
    "author": "B&B Team",
    "license": "LGPL-3",
    "depends": ["sale_management", "stock", "account", "mail", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",

        "views/sale_channel_views.xml",
        "views/credit_group_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/account_move_views.xml",
        "views/menus.xml",

        "report/credit_group_report.xml",
        "report/credit_group_report_template.xml"
    ],
    "installable": True,
    "application": False
}
