from odoo import models, fields, api

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.model
    def _selection_advance_payment_method(self):
        # Obtener órdenes de venta del contexto
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        
        # Verificar si hay anticipos previos
        has_deposits = any(
            line.is_downpayment 
            for order in sale_orders 
            for line in order.order_line
        )

        # Definir las opciones disponibles
        if has_deposits:
            # Si hay anticipos, solo mostrar percentage y fixed
            selection = [
                ('percentage', 'Anticipo (porcentaje)'),
                ('fixed', 'Anticipo (monto fijo)')
            ]
        else:
            # Si no hay anticipos, mostrar todas las opciones
            selection = [
                ('delivered', 'Pago completo'),
                ('percentage', 'Anticipo (porcentaje)'),
                ('fixed', 'Anticipo (monto fijo)')
            ]
        return selection

    advance_payment_method = fields.Selection(
        selection='_selection_advance_payment_method',
        string="Registrar pago",
        required=True,
        default='fixed'  # Cambiamos el default a 'fixed' ya que 'delivered' podría no estar disponible
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        
        # Verificar si hay anticipos previos
        has_deposits = any(
            line.is_downpayment 
            for order in sale_orders 
            for line in order.order_line
        )

        # Si hay anticipos previos, establecer valor por defecto a anticipo fijo
        if has_deposits:
            res['advance_payment_method'] = 'fixed'
            # Calcular monto restante
            for order in sale_orders:
                deposits_amount = sum(
                    line.price_unit 
                    for line in order.order_line 
                    if line.is_downpayment
                )
                remaining = order.amount_total - deposits_amount
                if remaining > 0:
                    res['fixed_amount'] = remaining
                    break

        return res