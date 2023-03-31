# -*- coding: utf-8 -*-
{
    'name': "helpdesk_route",

    'summary': """
       add route in helpdesk module """,

    'description': """
       add route in helpdesk module 
    """,

    'author': "Zargotel",
    'website': "https://www.zargotel.com",

    'category': 'Uncategorized',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'repair'
    ],

    # always loaded
    'data': [
        'views/route.xml'     
    ]
}
