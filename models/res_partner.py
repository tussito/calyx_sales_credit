from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_control = fields.Boolean(string="Control de crédito")
    credit_group_ids = fields.Many2many("calyx.credit.group", string="Grupos de crédito")

    @api.constrains("credit_control", "credit_group_ids")
    def _check_credit_groups_required(self):
        for rec in self:
            if rec.credit_control and not rec.credit_group_ids:
                raise ValidationError(_("Si el cliente tiene control de crédito, debe seleccionar al menos un grupo de crédito."))
