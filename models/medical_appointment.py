from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class MedicalAppointment(models.Model):
    _name = 'medical.appointment'
    _inherit = ['mail.thread']
    _description = 'Citas Médicas'

    name = fields.Char(string='Referencia', compute='_compute_name', store=True)
    patient_id = fields.Many2one('medical.patient', string='Paciente', required=True)
    doctor_id = fields.Many2one('medical.doctor', string='Doctor', required=True)
    document_search = fields.Char(string="Documento del Paciente")
    appointment_found = fields.Boolean(string="¿Tiene Cita?", compute="_compute_appointment_found", store=True)
    

    date = fields.Datetime(string='Fecha y Hora', required=True)
    state = fields.Selection([
        ('scheduled', 'Programada'),
        ('done', 'Realizada'),
        ('canceled', 'Cancelada'),
        ('no_show', 'No asistió')
    ], string='Estado', default='scheduled')

    notification_ids = fields.One2many('medical.notification', 'appointment_id', string='Notificaciones')

    @api.depends('patient_id', 'doctor_id', 'date')
    def _compute_name(self):
        """Genera un nombre automático para la cita."""
        for record in self:
            if record.patient_id and record.doctor_id and record.date:
                record.name = f"Cita {record.patient_id.name} - {record.doctor_id.name} ({record.date.strftime('%Y-%m-%d %H:%M')})"
            else:
                record.name = "Nueva Cita"

    @api.constrains('date', 'doctor_id', 'patient_id')
    def _check_appointment_uniqueness(self):
        """Evita que un paciente tenga más de una cita con el mismo doctor el mismo día."""
        for record in self:
            appointment_date = record.date.date()
            existing_appointments = self.env['medical.appointment'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('patient_id', '=', record.patient_id.id),
                ('date', '>=', datetime.combine(appointment_date, datetime.min.time())),
                ('date', '<=', datetime.combine(appointment_date, datetime.max.time())),
                ('id', '!=', record.id)
            ])
            if existing_appointments:
                raise ValidationError("El paciente ya tiene una cita con este doctor en la misma fecha.")

    def send_appointment_reminder(self):
        """Envía recordatorios de citas y registra la notificación"""
        now = datetime.now()
        tomorrow = now + timedelta(days=1)

        appointments = self.env['medical.appointment'].search([
            ('date', '>=', tomorrow.replace(hour=0, minute=0, second=0)),
            ('date', '<=', tomorrow.replace(hour=23, minute=59, second=59)),
            ('state', '=', 'scheduled')
        ])

        mail_template = self.env.ref('medical_backend.email_template_appointment_reminder')

        for appointment in appointments:
            if mail_template:
                try:
                    # Enviar correo
                    mail_template.send_mail(appointment.id, force_send=True)
                    
                    # Crear notificación
                    self.env['medical.notification'].create({
                        'appointment_id': appointment.id,
                        'status': 'sent',
                        'email_content': mail_template.body_html
                    })

                    _logger.info(f"Recordatorio enviado a {appointment.patient_id.email}")
                except Exception as e:
                    _logger.error(f"Error enviando recordatorio: {str(e)}")
                    self.env['medical.notification'].create({
                        'appointment_id': appointment.id,
                        'status': 'failed',
                        'email_content': f"Error: {str(e)}"
                    })
            else:
                _logger.error("No se encontró la plantilla de correo.")

    @api.depends('document_search')
    def _compute_appointment_found(self):
        """Verifica si hay una cita para el paciente con el documento ingresado"""
        for record in self:
            if record.document_search:
                patient = self.env['medical.patient'].search([('document_id', '=', record.document_search)], limit=1)
                if patient:
                    appointment = self.env['medical.appointment'].search([('patient_id', '=', patient.id)], limit=1)
                    record.appointment_found = bool(appointment)
                else:
                    record.appointment_found = False
    @api.model
    def action_search_appointment(self):
        """Busca una cita según el documento del paciente ingresado y devuelve datos en JSON"""
        self.ensure_one()
        patient = self.env['medical.patient'].search([('document_id', '=', self.document_search)], limit=1)
        if patient:
            appointment = self.env['medical.appointment'].search([('patient_id', '=', patient.id)], limit=1)
            if appointment:
                return {
                    'patient_id': appointment.patient_id.name,
                    'doctor_id': appointment.doctor_id.name,
                    'date': appointment.date.strftime('%Y-%m-%d %H:%M'),
                    'state': appointment.state
                }
        return {'error': 'No se encontró cita para este paciente'}
