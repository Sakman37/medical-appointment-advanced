{
    'name': 'Medical Appointment Advanced',
    'version': '1.0',
    'summary': 'Gestión avanzada de citas médicas en Odoo',
    'author': 'Sakman37',
    'category': 'Healthcare',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/medical_security.xml',
        'security/ir.model.access.csv',
        'views/admin_view.xml',
        'views/patient_view.xml',
        'views/patient_app_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/notification_view.xml',
        'data/email_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            
            'medicalbackend/static/src/js/appointment_form_widget.js',
            'medicalbackend/static/src/js/appointment_kanban_widget.js',
            'medicalbackend/static/src/js/appointment_statusbar_widget.js',
            'medicalbackend/static/src/js/medical_doctor.js',
            

            
            'medicalbackend/static/src/scss/medical_doctor.scss',
            'medicalbackend/static/src/scss/appointment_form.scss',
            'medicalbackend/static/src/scss/appointment_kanban.scss',
            'medicalbackend/static/src/scss/appointment_statusbar.scss',
        ],
        'web.assets_qweb': [
            'medicalbackend/static/src/xml/appointment_statusbar.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
