from odoo import models, _
from odoo.exceptions import UserError
import urllib.parse
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_send_whatsapp(self):
        self.ensure_one()

        if not self.partner_id.mobile:
            raise UserError(_('El cliente no tiene número de teléfono móvil registrado.'))

        try:
            if not self.access_token:
                self._portal_ensure_token()

            mobile = self.partner_id.mobile.replace(' ', '').replace('+', '').replace('-', '')
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            pdf_url = f"{base_url}/report/pdf/account.report_invoice_with_payments/{self.id}?access_token={self.access_token}"
            portal_url = f"{base_url}/my/invoices/{self.id}?access_token={self.access_token}"

            # Obtener datos del vehículo si hay orden relacionada
            sale_order = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)
            if sale_order:
                datos_vehiculo_template = _(
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
                )
                datos_vehiculo = datos_vehiculo_template.format(
                    marca=sale_order.marca_auto or '-',
                    nombre=sale_order.nombre_auto or '-',
                    modelo=sale_order.anio_auto or '-',
                    km=sale_order.kilometraje_auto or '-',
                    color=sale_order.color_auto or '-',
                    serie=sale_order.serie_auto or '-',
                    placas=sale_order.placas_auto or '-',
                    tanque=sale_order.tanque_gasolina or '-',
                    observaciones=sale_order.observations or '-',
                )
            else:
                datos_vehiculo = ""

            # Detalles de servicios/productos
            servicios = "\n".join([
                _("🔹 {name}\n    🔸 Cantidad: {qty}    💵 {total} {currency}").format(
                    name=line.name,
                    qty=line.quantity,
                    total=line.price_total,
                    currency=self.currency_id.name
                )
                for line in self.invoice_line_ids
            ])

            # Plantilla del mensaje principal
            message_template = _(
"""👋 ¡Hola {cliente}!

Tu orden *{orden}* está lista.

{datos_vehiculo}

🛠️ *Servicios realizados:*
{servicios}

💰 *Total:* {total} {moneda}

📄 Puedes descargar tu comprobante en PDF aquí:
{portal}

¿Tienes alguna pregunta? ¡Estamos para servirte! 😊"""
            )

            message = message_template.format(
                cliente=self.partner_id.name,
                orden=self.name,
                datos_vehiculo=datos_vehiculo,
                servicios=servicios,
                total=self.amount_total,
                moneda=self.currency_id.name,
                portal=portal_url
            )

            whatsapp_url = f"https://wa.me/{mobile}?text={urllib.parse.quote(message)}"

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_url,
                'target': 'new'
            }

        except Exception as e:
            _logger.error(f"Error al enviar: {str(e)}")
            raise UserError(_("Error al enviar mensaje: %s") % str(e))
