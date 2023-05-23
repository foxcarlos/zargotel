# -*- coding: utf-8 -*-
{
    'name': "report_invoce_extended",
    'summary': """Customized invoice report for Electronica Fernandez""",
    'description': """Customized invoice report for Electronica Fernandez""",
    'author': "Carlos Alberto Garcia Diaz",
    'website': "https://www.carlosgarciadiaz.com.ar",
    'category': 'Accounting/Accounting',
    'version': '0.1',
    'license': 'AGPL-3',
    'depends': ['account', 'sale_management'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_invoice.xml',
        # 'views/account_move.xml',
    ],
    'application': True,
    'installable': True,
    'development_status': "Alpha",
    'images': ["static/description/icon.png"],
    'maintainers': ["foxcarlos@gmail.com"],
}
