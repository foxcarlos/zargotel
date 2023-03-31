# -*- coding: utf-8 -*-
{
    'name': "helpdesk_to_rapair",
    'summary': """
        Module that allows exporting data from the HelpDesk module to the repair module.""",
    'description': """Module that allows exporting data from the HelpDesk module to the repair module""",
    'author': "Carlos Alberto Garcia Diaz",
    'website': "",
    'category': 'Helpdesk',
    'version': '0.1',
    "license": "AGPL-3",
    'depends': ['helpdesk_mgmt', 'repair'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_repair_wizard_view.xml',
        'views/helpdesk_view_inherit.xml',
        'views/repair_order_form_view.xml'
    ],
    "application": True,
    "installable": True,
    "development_status": "Alpha",
    "images": ["static/description/icon.png"],
    "maintainers": ["foxcarlos@gmail.com"],
}

