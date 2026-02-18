from odoo import fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    channel_id = fields.Many2one("calyx.sale.channel", string="Canal de Venta", readonly=True, copy=False)

    def _get_related_sale(self):
        self.ensure_one()
        # Usualmente picking viene de sale.order por group_id/origin
        if self.sale_id:
            return self.sale_id
        so = self.env["sale.order"].search([("name", "=", self.origin)], limit=1)
        return so

    def write(self, vals):
        res = super().write(vals)
        if "channel_id" not in vals:
            for p in self:
                so = p._get_related_sale()
                if so and so.channel_id and not p.channel_id:
                    p.channel_id = so.channel_id.id
        return res
