from odoo import models, fields, api

class MedicalAdmin(models.Model):
    _name = "medical.admin"
    _description = "Administración Médica"

    total_appointments = fields.Integer(string="Total de Citas", compute="_compute_appointments", store=True)
    canceled_appointments = fields.Integer(string="Citas Canceladas", compute="_compute_appointments", store=True)

    @api.depends("total_appointments", "canceled_appointments")
    def _compute_appointments(self):
        Appointment = self.env["medical.appointment"]
        for record in self:
            record.total_appointments = Appointment.search_count([])
            record.canceled_appointments = Appointment.search_count([("state", "=", "canceled")])
