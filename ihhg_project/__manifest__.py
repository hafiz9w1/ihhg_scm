{
    'name': "iHH Project",
    'version': "15.0.1.0.1",
    'category': 'project',
    'summary': """ Custom module""",

    'description': """
    Update for project part
    """,

    'author': "Hafiz Abbas",
    'email': "hafiz@portcities.net",
    'website': "http://portcities.net",
    'depends': [
        'base',
        'project',
        'project_enterprise',
        'ihhg_master',
    ],

    'data': [
        'security/ir.model.access.csv',
        'report/project_report.xml',
        'report/project_report_template.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/scm_entry_views.xml',
        'wizard/scm_entry_add_project_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
