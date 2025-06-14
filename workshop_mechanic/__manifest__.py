# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.comi
# facebook.com/dcrinformaticservices

{
    'name': "Automobile Auto Repair - ",  # Eliminado @ del nombre
    #modulo para rama 16
    'summary': """
        Module to efficiently manage your mechanical workshop.
        Keep detailed records of your customers' vehicles,
        optimize service administration and generate quick
        reports to visualize repair profit margins.
    """,

    'description': """
        This module expands Odoo's capabilities to provide a comprehensive
        solution for managing your mechanical workshop.

        Main features:
        * Automatic Vehicle Registration:
            - Vehicle Name
            - Make and Model
            - Vehicle registration
            - Color
            - Mileage
            - Fuel Tank Level

        * Vehicle History by Customer:
            - "Vehicles" section in customer profile
            - Storage of all registered vehicles

        * Quick Selection for Future Visits:
            - Saved vehicle selection
            - Mileage and fuel level updates
            - Optimized process without data re-entry
    """,

    'author': "DCR INFORMATIC SERVICES SAS DE CV",
    'maintainer': "DCR INFORMATIC SERVICES SAS DE CV",
    'website': "https://www.dcrsoluciones.com",
    'support': "soporte@dcrsoluciones.com",
    'license': 'LGPL-3',

    'category': 'Sales',
    'version': '16.0.1.0.0',
    'sequence': 1,

    'depends': [
        'base',
        'sale',
    ],

    'data': [
        'security/car_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views_inherit.xml',
        'views/sale_order.xml',
        'views/sale_order_views.xml',
        'views/account_inherit_view_margin.xml',
        'views/sale_whatsapp.xml',
        'views/account_move_whatsapp_button.xml',
        'views/vistamobil.xml',
        'views/car_model_menu.xml',
        'views/car_model_views.xml',
    ],

    'assets': {},
    
    'images': [
        'static/description/banner.gif',
        'static/description/icon.png'
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,

    'price': 32.33,
    'currency': 'EUR',
}