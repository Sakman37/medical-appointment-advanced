from odoo import models, fields, api
import uuid
import re
from odoo.exceptions import ValidationError

class MedicalPatient(models.Model):
    _name = "medical.patient"
    _description = "Patient"
    _inherit = "mail.thread"

    name = fields.Char(string="Nombre", required=True)
    email = fields.Char(string="Correo electrónico", required=True)
    document_id = fields.Char(string="Documento", required=True, unique=True)
    phone = fields.Char(string="Teléfono")
    age = fields.Integer(string="Edad", required=True)
    doctor_id = fields.Many2one("medical.doctor", string="Doctor")
    identifier = fields.Char(string="ID Paciente", readonly=True, copy=False, default=lambda self: str(uuid.uuid4()))
    user_id = fields.Many2one("res.users", string="Usuario", help="Usuario asociado al paciente")

    @api.model_create_multi  
    def create(self, vals_list):
        users = self.env["res.users"]
        patients = []
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        for vals in vals_list:
            
            if vals.get("age", 0) <= 0:
                raise ValidationError("La edad debe ser mayor a 0.")

            
            if "email" in vals:
                if not re.match(email_pattern, vals["email"]):
                    raise ValidationError("El correo electrónico no es válido.")

                existing_patient = self.env["medical.patient"].search([("email", "=", vals["email"])], limit=1)
                if existing_patient:
                    raise ValidationError("El correo ya está registrado para otro paciente.")

           
            if vals.get("email"):
                user_vals = {
                    "name": vals.get("name"),
                    "login": vals.get("email"),
                    "password": "123456",  # Contraseña por defecto
                    "groups_id": [(6, 0, [self.env.ref("medicalbackend.group_medical_patient").id])]
                    
                }
                user = users.create(user_vals)
                vals["user_id"] = user.id

            patients.append(vals)

        return super().create(patients)
