from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class MedicalNotification(models.Model):
    _name = 'medical.notification'
    _description = 'Notificaciones de Citas'
    
    appointment_id = fields.Many2one('medical.appointment', string='Cita Médica', required=True, ondelete='cascade')
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido')
    ], string='Estado', default='pending', required=True)
    email_content = fields.Text(string='Contenido del Correo', required=True)

    _sql_constraints = [
        ('unique_pending_notification', 
         'UNIQUE(appointment_id, status)', 
         'Ya existe una notificación pendiente para esta cita.')
    ]

    def send_notification(self):
        """ Enviar una notificación por correo si está pendiente """
        for record in self:
            if record.status != 'pending':
                continue
            
            try:
                mail_template = self.env.ref('medical_backend.email_template_appointment_reminder')
                if mail_template:
                    mail_template.send_mail(record.appointment_id.id, force_send=True)
                    record.status = 'sent'
                    _logger.info(f"Correo enviado para la cita {record.appointment_id.id}")
                else:
                    raise ValidationError("No se encontró la plantilla de correo.")

            except Exception as e:
                record.status = 'failed'
                _logger.error(f"Error enviando notificación: {str(e)}")

    @api.model
    def process_pending_notifications(self):
        """ Procesa todas las notificaciones pendientes en cola """
        pending_notifications = self.search([('status', '=', 'pending')])
        if pending_notifications:
            _logger.info(f"Procesando {len(pending_notifications)} notificaciones pendientes.")
            pending_notifications.send_notification()
        else:
            _logger.info("No hay notificaciones pendientes para procesar.")
