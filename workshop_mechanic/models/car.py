# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CarModel(models.Model):
    _name = 'car.model'
    _description = 'Car Model'

    name = fields.Char(string='Model Name', required=True )
    brand = fields.Selection(
        selection=[
            ('nissan', 'Nissan'),
            ('chevrolet', 'Chevrolet'),
            ('volkswagen', 'Volkswagen'),
            ('toyota', 'Toyota'),
            ('kia', 'Kia'),
            ('honda', 'Honda'),
            ('mazda', 'Mazda'),
            ('hyundai', 'Hyundai'),
            ('ford', 'Ford'),
            ('renault', 'Renault'),
            ('seat', 'SEAT'),
            ('bmw', 'BMW'),
            ('mercedes', 'Mercedes-Benz'),
            ('audi', 'Audi'),
            ('jeep', 'Jeep'),
            ('ram', 'RAM'), 
            ('crysler', 'Crysler'),
            ('cadillac', 'Cadillac'),
            ('gmc', 'GMC'),
            ('dodge', 'Dodge'),
            ('mitsubishi', 'Mitsubishi'),
            ('peugeot', 'Peugeot'),
            ('fiat', 'Fiat'),
            ('subaru', 'Subaru'),
            ('acura', 'Acura'),
            ('lincoln', 'Lincoln'),
            ('volvo', 'Volvo'),
            ('chirey', 'Chirey'),
            ('mg', 'MG'),
            ('jac', 'JAC'),
            ('baic', 'BAIC'),
            ('foton', 'Foton'),
            ('other', 'Otra marca'),
        ],
        string='Brand',
        required=True
    )


class Car(models.Model):
    _name = 'car'
    _description = 'Car'

    marca_auto = fields.Selection(
        selection=[
            ('nissan', 'Nissan'),
            ('chevrolet', 'Chevrolet'),
            ('volkswagen', 'Volkswagen'),
            ('toyota', 'Toyota'),
            ('kia', 'Kia'),
            ('honda', 'Honda'),
            ('mazda', 'Mazda'),
            ('hyundai', 'Hyundai'),
            ('ford', 'Ford'),
            ('renault', 'Renault'),
            ('seat', 'SEAT'),
            ('bmw', 'BMW'),
            ('mercedes', 'Mercedes-Benz'),
            ('audi', 'Audi'),
            ('jeep', 'Jeep'),
            ('ram', 'RAM'), 
            ('crysler', 'Crysler'),
            ('cadillac', 'Cadillac'),
            ('gmc', 'GMC'),
            ('dodge', 'Dodge'),
            ('mitsubishi', 'Mitsubishi'),
            ('peugeot', 'Peugeot'),
            ('fiat', 'Fiat'),
            ('subaru', 'Subaru'),
            ('acura', 'Acura'),
            ('lincoln', 'Lincoln'),
            ('volvo', 'Volvo'),
            ('chirey', 'Chirey'),
            ('mg', 'MG'),
            ('jac', 'JAC'),
            ('baic', 'BAIC'),
            ('foton', 'Foton'),
            ('other', 'Otra marca'),
        ],
        string='Brand',
        required=True,
    )

    nombre_auto = fields.Many2one(
        'car.model',
        string='Model',
        domain="[('brand', '=', marca_auto)]"
    )

    anio_auto = fields.Selection(
        selection=lambda self: self._get_years(),
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
    observations = fields.Text(string='Observation')
    partner_id = fields.Many2one('res.partner', string='Customer')

    @api.onchange('marca_auto')
    def _onchange_marca_auto(self):
        self.nombre_auto = False

    def name_get(self):
        result = []
        for record in self:
            brand = dict(self._fields['marca_auto'].selection).get(record.marca_auto, '')
            model = record.nombre_auto.name if record.nombre_auto else ''
            year = record.anio_auto or ''
            name = f"{brand} {model} ({year})"
            result.append((record.id, name.strip()))
        return result

    def _get_years(self):
        current_year = datetime.now().year
        years = []
        # Genera años desde 1990 hasta el año actual
        for year in range(current_year, 1989, -1):
            years.append((str(year), str(year)))
        return years

        