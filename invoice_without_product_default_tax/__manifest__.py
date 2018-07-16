# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
{
    'name': "Impuesto por defecto",
    'summary': """Carga de valores de Impuesto por defecto en facturas en las que no se seleccion producto""",
    'description': """
        Agrega campo Cuenta Analítica en Productos y Partner.
    """,
    'author': "Falcon Solutions SpA",
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'Account',
    'version': '10.0.1',
    'depends': ['sale','purchase','account'],
    'data': [
        #'views/account_invoice_view.xml',
    ],
    'demo': [
    ],
}
