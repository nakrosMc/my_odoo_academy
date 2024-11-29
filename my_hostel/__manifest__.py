{
    'name': "Hostel Management",
    'summary': "Manage Hostel easily",
    'description': "Efficiently manage the entire residential facility in the school.",  # Este campo soporta RST, pero puede ser mejor evitarlo.
    'author': "Nakros",
    'license': 'LGPL-3',
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    'depends': ['base'],
    'data': [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "views/hostel_student_view.xml",
        "views/hostel_room_view.xml",
        "views/hostel.xml",
        "views/hostel_category_view.xml",
        "views/room_copy_view.xml",
        "views/menu_views.xml",
        "data/data.xml"
    ],
    'installable': True,  # Asegúrate de que el módulo es instalable
    'auto_install': False,  # Esto es útil si no quieres que se instale automáticamente
}
