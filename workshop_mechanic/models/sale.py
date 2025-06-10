# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com


from odoo import api, fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_mobile = fields.Char(
        string="Mobile Phone",
        related="partner_id.mobile",
        store=True,
        readonly=False,
    )
    
    car_ids = fields.One2many(
        comodel_name='car',
        inverse_name='partner_id',
        string='Vehicles',
        readonly=False
    )

    selected_car_id = fields.Many2one(
        comodel_name='car',
        string='Selected Vehicle',
        help='Select the customers vehicle for this quote.',
        readonly=False
    )

    marca_auto = fields.Char(string='Brand')
    nombre_auto = fields.Char(string='Car Name')
    anio_auto = fields.Selection(
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
    observations = fields.Text(string='Observation')

    @api.onchange('selected_car_id')
    def _onchange_selected_car_id(self):
        if self.selected_car_id:
            self.marca_auto = self.selected_car_id.marca_auto
            self.nombre_auto = self.selected_car_id.nombre_auto
            self.anio_auto = self.selected_car_id.anio_auto
            self.color_auto = self.selected_car_id.color_auto
            self.kilometraje_auto = self.selected_car_id.kilometraje_auto
            self.placas_auto = self.selected_car_id.placas_auto
            self.tanque_gasolina = self.selected_car_id.tanque_gasolina
        else:
            self.marca_auto = False
            self.nombre_auto = False
            self.anio_auto = False
            self.color_auto = False
            self.kilometraje_auto = False
            self.placas_auto = False
            self.tanque_gasolina = False

    def _update_car_data(self, car_vals):
        """
        Actualiza los datos del vehículo tanto en el modelo car como en res.partner
        """
        if self.selected_car_id and self.partner_id:
            # Actualizar el vehículo existente con los nuevos datos
            self.selected_car_id.write(car_vals)
            return self.selected_car_id
        return False

    def write(self, vals):
        _logger.info(f"Values ​​received in write: {vals}")
        res = super(SaleOrder, self).write(vals)
        
        if any(field in vals for field in ['nombre_auto', 'marca_auto', 'anio_auto', 'color_auto', 'kilometraje_auto', 'placas_auto', 'tanque_gasolina']):
            car_vals = {
                'marca_auto': vals.get('marca_auto', self.marca_auto),
                'nombre_auto': vals.get('nombre_auto', self.nombre_auto),
                'anio_auto': vals.get('anio_auto', self.anio_auto),
                'color_auto': vals.get('color_auto', self.color_auto),
                'kilometraje_auto': vals.get('kilometraje_auto', self.kilometraje_auto),
                'placas_auto': vals.get('placas_auto', self.placas_auto),
                'tanque_gasolina': vals.get('tanque_gasolina', self.tanque_gasolina),
            }
            updated_car = self._update_car_data(car_vals)
            if updated_car:
                vals['selected_car_id'] = updated_car.id

        return res

    @api.model
    def create(self, vals):
        """
        Sobrescribe el método create para gestionar la creación/actualización de vehículos
        cuando se crea una nueva cotización.
        """
        _logger.info(f"Values ​​received in create: {vals}")
        
        # Preparar los valores del vehículo si hay datos
        if vals.get('partner_id') and any(field in vals for field in [
            'nombre_auto', 'marca_auto', 'anio_auto', 'color_auto',
            'kilometraje_auto', 'placas_auto', 'tanque_gasolina'
        ]):
            car_vals = {
                'partner_id': vals['partner_id'],
                'marca_auto': vals.get('marca_auto', ''),
                'nombre_auto': vals.get('nombre_auto', ''),
                'anio_auto': vals.get('anio_auto', ''),
                'color_auto': vals.get('color_auto', ''),
                'kilometraje_auto': vals.get('kilometraje_auto', 0),
                'placas_auto': vals.get('placas_auto', ''),
                'tanque_gasolina': vals.get('tanque_gasolina', '1/4 de tanque'),
            }

            # Si hay un vehículo seleccionado, actualizar ese
            if vals.get('selected_car_id'):
                existing_car = self.env['car'].browse(vals['selected_car_id'])
                if existing_car.exists():
                    existing_car.write(car_vals)
                    vals['selected_car_id'] = existing_car.id
            # Si no hay vehículo seleccionado pero hay datos de vehículo, crear uno nuevo
            else:
                new_car = self.env['car'].create(car_vals)
                vals['selected_car_id'] = new_car.id
                # Actualizar el partner con el nuevo vehículo
                partner = self.env['res.partner'].browse(vals['partner_id'])
                if partner:
                    partner.write({'car_ids': [(4, new_car.id, False)]})

        # Crear la orden de venta
        res = super(SaleOrder, self).create(vals)
        return res

    def _get_years(self):
        current_year = datetime.now().year
        years = []
        # Genera años desde 1990 hasta el año actual
        for year in range(current_year, 1989, -1):
            years.append((str(year), str(year)))
        return years