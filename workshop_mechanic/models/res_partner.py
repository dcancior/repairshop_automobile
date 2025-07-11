# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    car_ids = fields.One2many('car', 'partner_id', string=_('Vehículos'))
    