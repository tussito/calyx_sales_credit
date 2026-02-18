from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    channel_id = fields.Many2one("calyx.sale.channel", string="Canal de Venta", required=True)
    credit_state = fields.Selection([
        ("nolimit", "Sin límite de crédito"),
        ("available", "Crédito Disponible"),
        ("blocked", "Crédito bloqueado"),
    ], string="Crédito", compute="_compute_credit_state", store=False, readonly=True)

    @api.onchange("channel_id")
    def _onchange_channel_id(self):
        for order in self:
            if order.channel_id and order.channel_id.warehouse_id:
                order.warehouse_id = order.channel_id.warehouse_id

    def _find_credit_group(self):
        self.ensure_one()
        partner = self.partner_id
        if not partner or not partner.credit_control or not self.channel_id:
            return self.env["calyx.credit.group"]
        # Buscar grupo asignado al partner para este canal
        return partner.credit_group_ids.filtered(lambda g: g.channel_id.id == self.channel_id.id)[:1]

    @api.depends("partner_id", "channel_id", "amount_total", "currency_id")
    def _compute_credit_state(self):
        for order in self:
            order.credit_state = "nolimit"
            partner = order.partner_id
            if not partner or not partner.credit_control:
                continue
            group = order._find_credit_group()
            if not group:
                continue
            company = order.company_id
            date = order.date_order.date() if order.date_order else fields.Date.today()
            total_company = order.currency_id._convert(order.amount_total, company.currency_id, company, date)
            order.credit_state = "blocked" if total_company > group.credit_available else "available"

    def action_confirm(self):
        for order in self:
            if order.credit_state == "blocked":
                raise UserError(_("No se puede confirmar la venta: Crédito bloqueado."))
        return super().action_confirm()

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        if self.channel_id:
            vals["channel_id"] = self.channel_id.id
            if self.channel_id.journal_id:
                vals["journal_id"] = self.channel_id.journal_id.id
        return vals
