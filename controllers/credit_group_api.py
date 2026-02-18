from odoo import http
from odoo.http import request

class CreditGroupAPI(http.Controller):

    @http.route("/api/credit_groups", type="json", auth="public", csrf=False, methods=["POST"])
    def upsert_credit_groups(self, **kwargs):
        payload = request.jsonrequest or {}
        groups = payload.get("grupo_credititos") or payload.get("grupo_creditos") or payload.get("groups")
        if not isinstance(groups, list):
            return {"status": 400, "message": "JSON inválido"}

        CreditGroup = request.env["calyx.credit.group"].sudo()
        Channel = request.env["calyx.sale.channel"].sudo()

        for g in groups:
            code = (g or {}).get("codigo")
            name = (g or {}).get("name")
            channel_code = (g or {}).get("canal")
            credit_global = (g or {}).get("credito_global")

            channel = Channel.search([("code", "=", channel_code)], limit=1)
            if not channel:
                return {"status": 400, "message": f"No se encontro el canal {channel_code}"}

            rec = CreditGroup.search([("code", "=", code)], limit=1)
            vals = {
                "name": name,
                "channel_id": channel.id,
                "credit_global": credit_global,
                "company_id": request.env.company.id,
            }
            if rec:
                rec.write(vals)
            else:
                vals["code"] = code
                CreditGroup.create(vals)

        return {"status": 200, "message": "OK"}
