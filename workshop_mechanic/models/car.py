# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Car(models.Model):
    _name = 'car'
    _description = 'Car'
    marca_auto = fields.Char(string='Brand')
    nombre_auto = fields.Char(string='Car Name', required=False)
    #modelo_auto = fields.Char(string='Model')
    modelo_auto = fields.Selection(
        selection='_get_years',
        string='Model Year',
        help='Select the vehicle model year'
    )
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

    def _get_years(self):
        current_year = datetime.now().year
        years = []
        # Genera años desde 1950 hasta el año actual
        for year in range(current_year, 1989, -1):
            years.append((str(year), str(year)))
        return years