from odoo import http
from odoo.http import request
import json
from odoo.exceptions import ValidationError

class MedicalAPI(http.Controller):

    def _cors_response(self, data):
        """ Devuelve una respuesta JSON con los encabezados CORS configurados """
        response = request.make_response(json.dumps(data))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    @http.route('/api/admins', type='http', auth='public', cors="*")
    def get_medical_admins(self, **kwargs):
        admins = request.env['medical.admin'].sudo().search([])
        data = [
            {
                'id': admin.id,
                'user': admin.user_id.name,
                'total_appointments': admin.total_appointments,
                'completed_appointments': admin.completed_appointments,
                'canceled_appointments': admin.canceled_appointments
            }
            for admin in admins
        ]
        return self._cors_response(data)

    @http.route('/api/doctors', type='http', auth='public', cors="*")
    def get_doctors(self, **kwargs):
        doctors = request.env['medical.doctor'].sudo().search([])
        data = [
            {
                'id': doc.id,
                'name': doc.name,
                'specialization': doc.specialization,
                'phone': doc.phone,
                'day_of_week': doc.day_of_week,  
                'start_time': doc.start_time,  
                'end_time': doc.end_time
            }
            for doc in doctors
        ]
        return self._cors_response(data)

    @http.route('/api/appointments', type='http', auth='public', cors="*")
    def get_appointments(self, **kwargs):
        appointments = request.env['medical.appointment'].sudo().search([])
        data = [
            {
                'id': appt.id,
                'patient': appt.patient_id.name,
                'doctor': appt.doctor_id.name if appt.doctor_id else "No asignado",
                'date': appt.date,
                'state': appt.state
            }
            for appt in appointments
        ]
        return self._cors_response(data)

    @http.route('/api/patients', type='http', auth='public', cors="*")
    def get_patients(self, **kwargs):
        patients = request.env['medical.patient'].sudo().search([])
        data = [
            {
                'id': pat.id,
                'name': pat.name,
                'email': pat.email,
                'phone': pat.phone,
                'age': pat.age,
                'doctor': pat.doctor_id.name if pat.doctor_id else "No asignado",
                'identifier': pat.identifier
            }
            for pat in patients
        ]
        return self._cors_response(data)

    @http.route('/api/patients/create', type='http', auth='public', cors="*", methods=['POST'])
    def create_patient(self, **kwargs):
        try:
            required_fields = ["name", "email", "age"]
            for field in required_fields:
                if field not in kwargs:
                    return self._cors_response({"error": f"El campo {field} es obligatorio."})

            new_patient = request.env["medical.patient"].sudo().create({
                "name": kwargs["name"],
                "email": kwargs["email"],
                "phone": kwargs.get("phone", ""),
                "age": kwargs["age"],
                "doctor_id": kwargs.get("doctor_id", False)
            })

            return self._cors_response({
                "success": True,
                "message": "Paciente creado con éxito.",
                "patient_id": new_patient.id
            })

        except ValidationError as e:
            return self._cors_response({"error": str(e)})
        except Exception as e:
            return self._cors_response({"error": "Ocurrió un error inesperado.", "details": str(e)})

    @http.route('/api/notifications/<int:appointment_id>', type='http', auth='public', cors="*")
    def get_notifications(self, appointment_id, **kwargs):
        notifications = request.env['medical.notification'].sudo().search([
            ('appointment_id', '=', appointment_id)
        ])
        data = [
            {
                'id': notif.id,
                'appointment_id': notif.appointment_id.id,
                'status': notif.status,
                'email_content': notif.email_content
            }
            for notif in notifications
        ]
        return self._cors_response(data)

    @http.route('/api/notifications/create', type='http', auth='public', cors="*", methods=['POST'])
    def create_notification(self, **kwargs):
        try:
            required_fields = ["appointment_id", "email_content"]
            for field in required_fields:
                if field not in kwargs:
                    return self._cors_response({"error": f"El campo {field} es obligatorio."})

            new_notification = request.env["medical.notification"].sudo().create({
                "appointment_id": kwargs["appointment_id"],
                "email_content": kwargs["email_content"],
                "status": "pending"
            })

            return self._cors_response({
                "success": True,
                "message": "Notificación creada con éxito.",
                "notification_id": new_notification.id
            })

        except ValidationError as e:
            return self._cors_response({"error": str(e)})
        except Exception as e:
            return self._cors_response({"error": "Ocurrió un error inesperado.", "details": str(e)})

    @http.route('/api/notifications/send/<int:notification_id>', type='http', auth='public', cors="*")
    def send_notification(self, notification_id, **kwargs):
        try:
            notification = request.env['medical.notification'].sudo().browse(notification_id)
            if not notification:
                return self._cors_response({"error": "No se encontró la notificación."})

            if notification.status == "sent":
                return self._cors_response({"error": "Esta notificación ya fue enviada."})

            notification.send_notification()
            return self._cors_response({"success": True, "message": "Notificación enviada correctamente."})

        except ValidationError as e:
            return self._cors_response({"error": str(e)})
        except Exception as e:
            return self._cors_response({"error": "Ocurrió un error inesperado.", "details": str(e)})
