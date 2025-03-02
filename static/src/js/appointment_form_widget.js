/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";

export class AppointmentFormController extends FormController {
    setup() {
        super.setup();
        // Inicialización personalizada
    }
    
    /**
     * Personalización para manejar eventos de guardado
     * @override
     */
    async saveRecord() {
        // Código personalizado antes de guardar
        console.log("Guardando cita médica...");
        
        // Llamar al método original
        const result = await super.saveRecord(...arguments);
        
        // Código personalizado después de guardar
        console.log("Cita médica guardada exitosamente");
        
        return result;
    }
}

// Heredar la vista de formulario para usar nuestro controlador
export const AppointmentFormView = {
    ...formView,
    Controller: AppointmentFormController,
};

// Registrar la vista para el modelo específico
registry.category("views").add("appointment_form_view", AppointmentFormView);