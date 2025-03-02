/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";

// Personalizar KanbanRecord
export class AppointmentKanbanRecord extends KanbanRecord {
    /**
     * @override
     */
    setup() {
        super.setup();
        this.dateFormat = "DD/MM/YYYY HH:mm";
    }

    /**
     * Personalizar la visualización de cada tarjeta después del renderizado
     * @override
     */
    onRendered() {
        super.onRendered();
        
        // Agregar clases según el estado
        const state = this.props.record.data.state;
        if (state) {
            const cardEl = this.el.querySelector('.appointment-card');
            if (cardEl) {
                cardEl.classList.add(`appointment-${state}`);
            }
        }
        
        // Formatear fecha si es necesario
        const dateEl = this.el.querySelector('.date-field');
        if (dateEl && this.props.record.data.date) {
            const formattedDate = this.formatDateTime(this.props.record.data.date);
            dateEl.innerHTML = `<i class="fa fa-calendar"></i> ${formattedDate}`;
        }
    }
    
    /**
     * Formatear fecha/hora
     * @param {string} dateTime - Fecha/hora en formato ISO
     * @returns {string} - Fecha formateada
     */
    formatDateTime(dateTime) {
        return luxon.DateTime.fromISO(dateTime).toFormat(this.dateFormat);
    }
}

// Personalizar Renderer para usar nuestro Record
export class AppointmentKanbanRenderer extends KanbanRenderer {
    /**
     * @override
     */
    setup() {
        super.setup();
        this.KanbanRecord = AppointmentKanbanRecord;
    }
}

// Personalizar Controller
export class AppointmentKanbanController extends KanbanController {
    /**
     * @override
     */
    setup() {
        super.setup();
        // Personalización adicional
    }
}

// Personalizar Vista Kanban
export const AppointmentKanbanView = {
    ...kanbanView,
    Controller: AppointmentKanbanController,
    Renderer: AppointmentKanbanRenderer,
};

// Registrar la vista personalizada
registry.category("views").add("appointment_kanban_view", AppointmentKanbanView);