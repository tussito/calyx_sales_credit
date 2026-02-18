from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    channel_id = fields.Many2one("calyx.sale.channel", string="Canal de Venta", readonly=False)
