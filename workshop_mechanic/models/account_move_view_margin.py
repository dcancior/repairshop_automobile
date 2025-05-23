# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    margin = fields.Monetary(
        string='Margin',
        compute='_compute_margin',
        store=True,
        help='Total margin inherited from the sales order'
    )

    @api.depends('invoice_line_ids.sale_line_ids.margin')
    def _compute_margin(self):
        for move in self:
            total_margin = 0.0
            if move.move_type in ('out_invoice', 'out_refund'):
                for line in move.invoice_line_ids:
                    margins = line.sale_line_ids.mapped('margin')
                    total_margin += sum(margins) if margins else 0.0
            move.margin = total_margin