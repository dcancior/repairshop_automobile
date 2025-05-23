# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

# from odoo import http


# class TallerMecanico(http.Controller):
#     @http.route('/taller_mecanico/taller_mecanico', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/taller_mecanico/taller_mecanico/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('taller_mecanico.listing', {
#             'root': '/taller_mecanico/taller_mecanico',
#             'objects': http.request.env['taller_mecanico.taller_mecanico'].search([]),
#         })

#     @http.route('/taller_mecanico/taller_mecanico/objects/<model("taller_mecanico.taller_mecanico"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('taller_mecanico.object', {
#             'object': obj
#         })
