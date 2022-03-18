{
    'name': "iHH Group Custom Addon",
    'version': "15.0.1.0.1",
    'category': 'management',
    'summary': """ Custom module""",

    'description': """
    This module adds the following functionalities to extend the project Module.

Functionalities:
- Extend project model to add selection_criteria_id, scm_entry_id models
- Extend project model to add project_date_deadline for projects
- Extend res_partner to accommodate new address fields
- Channels model and view
- SCM Entry model and view
    * Filtering for Channel, Package and Item selection
    * Channel, Package and Item count
    * Visibility Calendar
    * SCM States
    * SCM Lock
    * Access Rights

- Package model and view
    * Item count
- SCM Package Line model and view
- SCM Item Line model and view
    * Item line model and view for SCM item selection
    * Package line creation automation from item line creation
- Item Tags model and view
- Category model and view
- Campaign type model and view

    """,

    'author': "Hafiz Abbas",
    'email': "hafiz@portcities.net",
    'website': "http://portcities.net",
    'depends': [
        'product',
        'project',
        'account',
        'stock',
    ],

    'data': [
        'security/scm_security.xml',
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/package_item_views.xml',
        'views/package_views.xml',
        'views/channel_views.xml',
        'views/scm_entry_item_line_views.xml',
        'views/scm_entry_package_line_views.xml',
        'views/category_views.xml',
        'views/campaign_type_views.xml',
        'views/item_tags_views.xml',
        'views/scm_entry_views.xml',
        'views/res_partner_views.xml',
        'views/menu_items.xml',
        'wizard/scm_entry_add_package_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
