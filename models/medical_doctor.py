import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MedicalDoctor(models.Model):
    _name = 'medical.doctor'
    _description = 'Doctores'

    name = fields.Char(string='Nombre', required=True)
    email = fields.Char(string="Correo Electrónico", required=True)
    specialization = fields.Char(string='Especialización', required=True)
    phone = fields.Char(string='Teléfono')

    day_of_week = fields.Selection([
        ('monday', 'Lunes'),
        ('tuesday', 'Martes'),
        ('wednesday', 'Miércoles'),
        ('thursday', 'Jueves'),
        ('friday', 'Viernes'),
        ('saturday', 'Sábado'),
        ('sunday', 'Domingo')
    ], string='Día de la Semana', required=True)

    start_time = fields.Float(string='Hora de Inicio', required=True)
    end_time = fields.Float(string='Hora de Fin', required=True)

    patient_ids = fields.One2many(
        'medical.patient',
        'doctor_id',
        string='Pacientes Atendidos'
    )

    user_id = fields.Many2one(
        'res.users', 
        string="Usuario de Odoo", 
        required=True,
        help="Usuario vinculado al doctor para iniciar sesión"
    )

    

    @api.constrains('day_of_week', 'start_time', 'end_time')
    def _check_schedule(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")

            # Verificar si el mismo doctor tiene otro horario en el mismo día con conflicto
            existing_schedules = self.env['medical.doctor'].search([
                ('id', '!=', record.id),
                ('name', '=', record.name),
                ('day_of_week', '=', record.day_of_week),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time)
            ])

            if existing_schedules:
                raise ValidationError(f"El doctor {record.name} ya tiene una disponibilidad en {dict(self._fields['day_of_week'].selection).get(record.day_of_week)} en ese horario.")

    @api.model_create_multi
    def create(self, vals_list):
        users = self.env["res.users"]
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        doctors = []

        for vals in vals_list:
            
            if not re.match(email_pattern, vals.get("email", "")):
                raise ValidationError("El correo electrónico no es válido.")

            
            existing_doctor = self.env["medical.doctor"].search([("email", "=", vals["email"])], limit=1)
            if existing_doctor:
                raise ValidationError("El correo ya está registrado para otro doctor.")

            
            user_vals = {
                "name": vals.get("name"),
                "login": vals.get("email"),
                "password": "123456",  # Contraseña por defecto
                "groups_id": [(6, 0, [self.env.ref("medicalbackend.group_medical_doctor").id])]
                
            }
            user = users.create(user_vals)
            vals["user_id"] = user.id

            doctors.append(vals)

        return super().create(doctors)
