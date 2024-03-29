# -*- coding: utf-8 -*-
{
    'name': "truffleapp",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Luis",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/categoryview.xml',
        'views/qualityview.xml',
        'views/weightview.xml',
        'views/productview.xml',
        'views/facturaview.xml',
        'views/orderview.xml',
        'views/invoiceTemplate.xml',
        'report/invoiceReport.xml',
        'security/rules.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
    'instalable':True,
}
