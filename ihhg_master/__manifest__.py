{
    'name': "iHH Group Custom Addon",
    'version': "15.0.1.0.0",
    'category': 'management',
    'summary': """ Custom module""",

    'description': """
    This module adds the following functionalities to extend the project Module.

Functionalities:
- Extend project model to add selection_criteria_id, scm_entry_id models
- Extend project model to add project_date_deadline for projects and function to update task date_deadline based on project_date_deadline
- Extend res_partner to accommodate new address fields
- Channels model and view
- SCM Entry model and view
- Selection Criteria model and view
- Store Regulation Entry model and view

    """,

    'author': "Hafiz Abbas",
    'email': "hafiz@portcities.net",
    'website': "http://portcities.net",
    'depends': ['project', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/channel_views.xml',
        'views/project_views.xml',
        'views/res_partner_views.xml',
        'views/scm_entry_views.xml',
        'views/selection_criteria_views.xml',
        'views/store_regulation_entry_views.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
