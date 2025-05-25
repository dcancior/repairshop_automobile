from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_anticipos = fields.Monetary(
        string='Total Anticipos',
        compute='_compute_anticipos',
        store=True,
        currency_field='currency_id',
        help='Suma total de los anticipos realizados'
    )

    restante_orden = fields.Monetary(
        string="Monto Restante",
        compute='_calculolar_monto_restante',
        store=True,
        currency_field='currency_id',
        help='Monto restante por pagar'
    )

    @api.depends('order_line.price_total', 'amount_total')
    def _compute_anticipos(self):
        for order in self:
            # Filtrar líneas que son anticipos (productos que se llaman exactamente "Anticipo")
            anticipos = order.order_line.filtered(
                lambda line: line.product_id.name 
                and line.product_id.name.strip() == 'Anticipo'
            )
            
            # Calcular total de anticipos usando el precio unitario
            total_anticipos = sum(line.price_unit for line in anticipos)
            order.total_anticipos = total_anticipos

            # Calcular monto restante
            order.restante_orden = order.amount_total - total_anticipos

            
    