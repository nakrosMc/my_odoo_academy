{
    'name': "Hostel Management",
    'summary': "Manage Hostel easily",
    'description': "Efficiently manage the entire residential facility in the school.",  # Este campo soporta RST, pero puede ser mejor evitarlo.
    'author': "Nakros",
    'license': 'LGPL-3',
    'website': "http://www.example.com",
    'category': 'hostel',
    'version': '18.0.0.1',
    'depends': ['base', 'mail'],
    'data': [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/datatxt.xml",
        "data/config.xml",
        "data/model_registration.xml",
        "data/hostel_stage_data.xml",
        "views/student_wizard_view.xml",
        "views/hostel_student_view.xml",
        "views/hostel_room_view.xml",
        "views/hostel_amenities_view.xml",
        "views/hostel.xml",
        "views/hostel_category_view.xml",
        "views/room_member_view.xml",
        "views/room_copy_view.xml",
        "views/partner_herenci_view.xml",
        'views/hostel_room_availability_views.xml',
        "views/res_config_settings_views.xml",
        "views/hostel_stage_view.xml",
        "views/menu_views.xml",
        "reports/hostel_room_detail_report_template.xml"
    ],
    'demo': [
    'data/demo.xml',
    ],
    'post_init_hook': 'add_room_hook',
    'pre_init_hook': 'pre_init_hook_hostel',
    'uninstall_init_hook': 'uninstall_hook_user',
    'installable': True,  # Asegúrate de que el módulo es instalable
    'auto_install': False,  # Esto es útil si no quieres que se instale automáticamente
}
