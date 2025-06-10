from odoo import models, fields, api
from odoo.exceptions import UserError
import urllib.parse
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_mobile = fields.Char(
        string="Teléfono Móvil",
        related="partner_id.mobile",
        store=True,
        readonly=False,
    )

    def action_send_whatsapp(self):
        """Enviar mensaje de WhatsApp notificando que la cotización está lista, con detalles de productos, vehículo y links de acceso"""
        self.ensure_one()
        
        if not self.partner_mobile:
            raise UserError('El cliente no tiene número de teléfono móvil registrado.')

        try:
            # Asegurar que exista access_token para acceso público
            if not self.access_token:
                self._portal_ensure_token()

            # Formatear el número de teléfono
            mobile = self.partner_mobile.replace(' ', '').replace('+', '').replace('-', '')

            # Crear lista de productos cotizados
            productos = "\n".join([
                f"🔹 {line.product_id.name}\n    🔸 Cantidad: {line.product_uom_qty}    💵 {line.price_total} {self.currency_id.name}"
                for line in self.order_line
            ])

            # Datos del vehículo
            datos_vehiculo = f"""
🚗 *Datos del Vehículo:*
• Nombre: {self.nombre_auto or '-'}
• Marca: {self.marca_auto or '-'}
• Modelo: {self.anio_auto or '-'}
• Kilometraje: {self.kilometraje_auto or '-'} km
• Placas: {self.placas_auto or '-'}
• Tanque de gasolina: {self.tanque_gasolina or '-'}
""" 
            # Generar links de acceso con access_token
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            pdf_url = f"{base_url}/report/pdf/sale.report_saleorder/{self.id}?access_token={self.access_token}"
            portal_url = f"{base_url}/my/orders/{self.id}?access_token={self.access_token}"

            # Crear el mensaje de WhatsApp
            message = f"""👋 ¡Hola {self.partner_id.name}!

Tu cotización *{self.name}* está lista. Aquí tienes los detalles:

{datos_vehiculo}

🛠️ *Servicios cotizados:*
{productos}

💰 *Total:* {self.amount_total} {self.currency_id.name}

📄 Puedes revisar tu cotización en el siguiente link:
{portal_url}

¿Tienes alguna pregunta? ¡Estamos para servirte! 😊🔧"""

            # Crear la URL de WhatsApp
            whatsapp_url = f"https://wa.me/{mobile}?text={urllib.parse.quote(message)}"
            # Marcar la cotización como enviada
            self.write({'state': 'sent'})
            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'target': 'new'
            }

        except Exception as e:
            _logger.error(f"Error al enviar: {str(e)}")
            raise UserError(f"Error al enviar mensaje: {str(e)}")