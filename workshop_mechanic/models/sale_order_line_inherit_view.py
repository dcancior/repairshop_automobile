# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    purchase_price = fields.Float(
        string=_('Precio de compra'),
        digits='Product Price',
        store=True
    )

    margin = fields.Float(
        string=_('Margen'),
        compute='_compute_margin',
        store=True
    )

    @api.depends('price_unit', 'product_uom_qty', 'discount', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            discount = line.discount or 0.0
            purchase_price = line.purchase_price or 0.0
            price = line.price_unit * (1 - discount / 100.0)
            line.margin = (price - purchase_price) * line.product_uom_qty

    @api.onchange('product_id')
    def _onchange_product_id_set_purchase_price(self):
        for line in self:
            if line.product_id:
                line.purchase_price = line.product_id.standard_price or 0.0

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    margin = fields.Monetary(
        string=_('Margen'),
        compute='_compute_margin',
        store=True
    )

    @api.depends('order_line.margin')
    def _compute_margin(self):
        for order in self:
            order.margin = sum(line.margin or 0.0 for line in order.order_line)
