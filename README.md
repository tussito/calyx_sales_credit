# calyx_sales_credit (Odoo 15)

- Canales de venta con depósito y diario + código por secuencia (CH000001...)
- Chatter con auditoría de cambios de nombre (tracking en `name`)
- Canal obligatorio en órdenes de venta; al cambiar canal se actualiza el depósito (warehouse)
- Facturas desde ventas usan el diario del canal y heredan el canal
- Canal visible/filtrable en órdenes de entrega (stock.picking) y facturas (account.move)
- Grupos de crédito por canal con: crédito global, utilizado (SO confirmadas sin facturar + facturas impagas), disponible
- Cliente con control de crédito + selección obligatoria de grupo
- Campo `Crédito` en la venta (nolimit/available/blocked) con badge y bloqueo al confirmar
- Reporte PDF del grupo (clientes + órdenes + facturas consideradas)
- Endpoint JSON POST `/api/credit_groups` para upsert por código con validación de canal

## Endpoint
POST `/api/credit_groups` (Content-Type: application/json)
```json
{
  "grupo_credititos": [
    {"name":"Grupo 1","codigo":"00001","canal":"CH000001","credito_global":500000}
  ]
}
```

Respuestas:
- Error canal: `{"status":400,"message":"No se encontro el canal CH000001"}`
- OK: `{"status":200,"message":"OK"}`
