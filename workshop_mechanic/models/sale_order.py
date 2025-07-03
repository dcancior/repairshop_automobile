from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    car_description = fields.Char(
        string='Vehículo',
        compute='_compute_car_description',
        store=True
    )

    def _compute_car_description(self):
        for order in self:
            parts = []
            # Si es Many2one, usa .name
            if order.marca_auto:
                parts.append(order.marca_auto.name if hasattr(order.marca_auto, 'name') else str(order.marca_auto))
            if order.nombre_auto:
                parts.append(order.nombre_auto.name if hasattr(order.nombre_auto, 'name') else str(order.nombre_auto))
            if order.anio_auto:
                parts.append(str(order.anio_auto))
            order.car_description = ' '.join(parts) if parts else ''