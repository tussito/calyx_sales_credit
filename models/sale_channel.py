from odoo import api, fields, models

class SaleChannel(models.Model):
    _name = "calyx.sale.channel"
    _description = "Canal de Venta"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "code desc, id desc"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(string="Código", readonly=True, copy=False, index=True, default="/")
    warehouse_id = fields.Many2one("stock.warehouse", string="Depósito", required=True)
    journal_id = fields.Many2one(
        "account.journal",
        string="Diario de factura",
        domain="[('type', '=', 'sale')]",
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env.ref("calyx_sales_credit.seq_sale_channel", raise_if_not_found=False)
        for vals in vals_list:
            if vals.get("code", "/") in ("/", False, None):
                vals["code"] = seq.next_by_id() if seq else self.env["ir.sequence"].next_by_code("calyx.sale.channel") or "CH000001"
        return super().create(vals_list)
