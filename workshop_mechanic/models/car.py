# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import fields, models

class Car(models.Model):
    _name = 'car'
    _description = 'Car'

    nombre_auto = fields.Char(string='Car Name', required=False)
    marca_auto = fields.Char(string='Brand')
    modelo_auto = fields.Integer(string='Model')
    color_auto = fields.Char(string='Color')
    kilometraje_auto = fields.Integer(string='Odometer')
    placas_auto = fields.Char(string='Vehicle registration')
    tanque_gasolina = fields.Selection(
        selection=[
            ('1/4 de tanque', '1/4 tank'),
            ('Medio tanque', 'Half tank'),
            ('3/4 de tanque', '3/4 tank'),
            ('Lleno', 'Full'),
        ],
        string='Fuel tank'
    )
    partner_id = fields.Many2one('res.partner', string='Customer')

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.nombre_auto} ({record.marca_auto} {record.modelo_auto})"
            result.append((record.id, name))
        return result