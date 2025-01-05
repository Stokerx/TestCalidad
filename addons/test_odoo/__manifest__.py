{
    'name': 'Test Odoo',
    'version': '1.0',
    'category': 'Uncategorized',
    'summary': 'Módulo para prueba de programación Odoo',
    'description': """
        Este módulo resuelve los requerimientos de la prueba de programación Odoo.
    """,
    'author': 'Luis Luna',
    'website': '',
    'depends': ['point_of_sale', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_order.xml',
        'views/account_move_views.xml',
        'views/sale_channel_views.xml',
        'reports/account_move_reports.xml',
        'data/sale_channel_data.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'test_odoo/static/src/js/pos.js',
            'test_odoo/static/src/xml/pos.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}