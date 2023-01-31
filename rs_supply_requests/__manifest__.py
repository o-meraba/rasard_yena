# -*- coding: utf-8 -*-
{
    'name': "rs_supply_requests",

    'summary': """
        Sale  Order to Purchase Order""",

    'description': """
        SO2REQ > REQ2PO
    """,

    'author': "Rasard Technology",
    'website': "http://rasard.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale_management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'purchase','rs_yena_so2po_test','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/supply_requests_views.xml',
        'views/sale_views.xml',
    ],
    "installable": True,
    
}
