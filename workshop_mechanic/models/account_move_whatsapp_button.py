from odoo import models
from odoo.exceptions import UserError
import urllib.parse
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_send_whatsapp(self):
        self.ensure_one()
        if not self.partner_id.mobile:
            raise UserError('El cliente no tiene número de teléfono móvil registrado.')

        try:
            # Asegurar que exista access_token
            if not self.access_token:
                self._portal_ensure_token()

            mobile = self.partner_id.mobile.replace(' ', '').replace('+', '').replace('-', '')
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            pdf_url = f"{base_url}/report/pdf/account.report_invoice_with_payments/{self.id}?access_token={self.access_token}"
            portal_url = f"{base_url}/my/invoices/{self.id}?access_token={self.access_token}"

            # Buscar la orden de venta relacionada para obtener los datos del vehículo
            sale_order = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)
            if sale_order:
                datos_vehiculo = f"""
🚗 *Datos del Vehículo:*
• Nombre: {sale_order.nombre_auto or '-'}
• Marca: {sale_order.marca_auto or '-'}
• Modelo: {sale_order.modelo_auto or '-'}
• Kilometraje: {sale_order.kilometraje_auto or '-'} km
• Placas: {sale_order.placas_auto or '-'}
• Tanque de gasolina: {sale_order.tanque_gasolina or '-'}
"""
            else:
                datos_vehiculo = ""

            # Servicios/productos facturados
            servicios = "\n".join([
                f"🔹 {line.name}\n    🔸 Cantidad: {line.quantity}    💵 {line.price_total} {self.currency_id.name}"
                for line in self.invoice_line_ids
            ])

            message = f"""👋 ¡Hola {self.partner_id.name}!

Tu orden *{self.name}* está lista.

{datos_vehiculo}

🛠️ *Servicios realizados:*
{servicios}

💰 *Total:* {self.amount_total} {self.currency_id.name}

📄 Puedes descargar tu comprobante en PDF aquí:
{portal_url}


¿Tienes alguna pregunta? ¡Estamos para servirte! 😊"""

            whatsapp_url = f"https://wa.me/{mobile}?text={urllib.parse.quote(message)}"

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'target': 'new'
            }
        except Exception as e:
            _logger.error(f"Error al enviar: {str(e)}")
            raise UserError(f"Error al enviar mensaje: {str(e)}")