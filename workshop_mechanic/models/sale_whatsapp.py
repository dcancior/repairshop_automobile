from odoo import models, fields, api, _
from odoo.exceptions import UserError
import urllib.parse
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_mobile = fields.Char(
        string=_("Teléfono Móvil"),
        related="partner_id.mobile",
        store=True,
        readonly=False,
    )

    def action_send_whatsapp(self):
        self.ensure_one()

        if not self.partner_mobile:
            raise UserError(_('El cliente no tiene número de teléfono móvil registrado.'))

        try:
            if not self.access_token:
                self._portal_ensure_token()

            mobile = self.partner_mobile.replace(' ', '').replace('+', '').replace('-', '')

            productos = "\n".join([
                _("🔹 {nombre}\n    🔸 Cantidad: {cantidad}    💵 {precio} {moneda}").format(
                    nombre=line.product_id.name or '',
                    cantidad=line.product_uom_qty or 0,
                    precio=line.price_total or 0.0,
                    moneda=self.currency_id.name or ''
                )
                for line in self.order_line
            ])

            datos_vehiculo = _(
                """🚗 *Datos del Vehículo:*
• Marca: {marca}
• Nombre: {nombre}
• Modelo: {modelo}
• Kilometraje: {km} km
• Color: {color}
• Número de serie: {serie}
• Placas: {placas}
• Tanque de gasolina: {tanque}
• Observaciones: {observaciones}
"""
            ).format(
                marca=self.marca_auto or '-',
                nombre=self.nombre_auto.name if self.nombre_auto else '-',
                modelo=self.anio_auto or '-',
                km=self.kilometraje_auto or '-',
                color=self.color_auto or '-',
                serie=self.serie_auto or '-',
                placas=self.placas_auto or '-',
                tanque=self.tanque_gasolina or '-',
                observaciones=self.observations or '-',
            )

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            pdf_url = f"{base_url}/report/pdf/sale.report_saleorder/{self.id}?access_token={self.access_token}"
            portal_url = f"{base_url}/my/orders/{self.id}?access_token={self.access_token}"

            message = _(
                """👋 ¡Hola {cliente}!

Tu cotización *{cotizacion}* está lista. Aquí tienes los detalles:

{datos_vehiculo}

🛠️ *Servicios cotizados:*
{productos}

💰 *Total:* {total} {moneda}

📄 Puedes revisar tu cotización en el siguiente link:
{link}

¿Tienes alguna pregunta? ¡Estamos para servirte! 😊🔧"""
            ).format(
                cliente=self.partner_id.name or '',
                cotizacion=self.name or '',
                datos_vehiculo=datos_vehiculo,
                productos=productos,
                total=self.amount_total or 0.0,
                moneda=self.currency_id.name or '',
                link=portal_url
            )

            whatsapp_url = f"https://wa.me/{mobile}?text={urllib.parse.quote(message)}"
            self.write({'state': 'sent'})

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'target': 'new'
            }

        except Exception as e:
            _logger.error(f"Error al enviar: {str(e)}")
            raise UserError(_('Error al enviar mensaje: {}').format(str(e)))
