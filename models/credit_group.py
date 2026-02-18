from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CreditGroup(models.Model):
    _name = "calyx.credit.group"
    _description = "Grupo de Crédito"
    _order = "code asc, id desc"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    channel_id = fields.Many2one("calyx.sale.channel", string="Canal de Venta", required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(related="company_id.currency_id", store=True, readonly=True)

    credit_global = fields.Monetary(string="Crédito global", currency_field="currency_id", required=True)
    credit_used = fields.Monetary(string="Crédito utilizado", currency_field="currency_id", compute="_compute_credit", store=False)
    credit_available = fields.Monetary(string="Crédito disponible", currency_field="currency_id", compute="_compute_credit", store=False)

    _sql_constraints = [
        ("credit_group_code_uniq", "unique(code)", "El código del grupo no debe repetirse."),
    ]

    @api.constrains("code")
    def _check_code(self):
        for rec in self:
            if not rec.code:
                continue
            if "026" in rec.code:
                raise ValidationError(_("El código no puede contener la secuencia '026'."))

    def _partners_domain(self):
        return [
            ("credit_control", "=", True),
            ("credit_group_ids", "in", self.ids),
        ]

    def _get_partners(self):
        self.ensure_one()
        return self.env["res.partner"].search(self._partners_domain())

    def _get_open_orders(self):
        self.ensure_one()
        partners = self._get_partners()
        if not partners:
            return self.env["sale.order"]
        # Confirmadas sin facturar (o parcialmente): state = sale/done, invoice_status != invoiced
        return self.env["sale.order"].search([
            ("partner_id", "in", partners.ids),
            ("channel_id", "=", self.channel_id.id),
            ("state", "in", ["sale", "done"]),
            ("invoice_status", "!=", "invoiced"),
        ])

    def _get_unpaid_invoices(self):
        self.ensure_one()
        partners = self._get_partners()
        if not partners:
            return self.env["account.move"]
        # Facturas impagas asociadas a clientes del grupo
        return self.env["account.move"].search([
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("partner_id", "in", partners.ids),
            ("payment_state", "in", ["not_paid", "partial"]),
            ("channel_id", "=", self.channel_id.id),
        ])

    @api.depends("credit_global", "channel_id")
    def _compute_credit(self):
        for rec in self:
            company = rec.company_id
            company_currency = company.currency_id

            used = 0.0

            for so in rec._get_open_orders():
                date = so.date_order.date() if so.date_order else fields.Date.today()
                used += so.currency_id._convert(so.amount_total, company_currency, company, date)

            for inv in rec._get_unpaid_invoices():
                date = inv.invoice_date or inv.date or fields.Date.today()
                used += inv.currency_id._convert(inv.amount_residual, company_currency, company, date)

            rec.credit_used = used
            rec.credit_available = rec.credit_global - used
