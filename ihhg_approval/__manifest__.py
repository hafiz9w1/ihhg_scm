{
    'name': "iHH Group Custom Addon - Approval",
    'version': "15.0.1.0.1",
    'category': 'management',
    'summary': """ Custom module""",

    'description': """
    This module adds the following functionalities to extend the approval Module.

Functionalities:
- Extend approval category for has_scm
- Extend Approval request for scm_entry_id
    - Function to log message in SCM chatter on approval submission

    """,

    'author': "Hafiz Abbas",
    'email': "hafiz@portcities.net",
    'website': "http://portcities.net",
    'depends': [
        'ihhg_master',
        'approvals',
    ],

    'data': [
        'views/approval_category_views.xml',
        'views/approval_request_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
