/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { useService } from "@web/core/utils/hooks";

class MedicalDoctorKanbanRecord extends KanbanRecord {
    setup() {
        super.setup();
        this.action = useService("action");
        this.notification = useService("notification");
    }

    /**
     * @override
     */
    get templateName() {
        return "medicalbackend.MedicalDoctorKanbanRecord";
    }

    /**
     * Gestiona el evento de clic en el botón de citas
     * @param {Event} ev
     */
    onClickAppointments(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        this._openAppointmentsView();
    }

    /**
     * Gestiona el evento de clic en el botón de mensaje
     * @param {Event} ev
     */
    onClickMessage(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        this._openMessageComposer();
    }

    /**
     * Abre la vista de citas filtrada por el doctor actual
     * @private
     */
    _openAppointmentsView() {
        const record = this.props.record.data;
        this.action.doAction({
            name: `Citas del Dr. ${record.name}`,
            type: 'ir.actions.act_window',
            res_model: 'medical.appointment',
            view_mode: 'calendar,list,form',
            domain: [['doctor_id', '=', record.resId]],
            context: {
                'default_doctor_id': record.resId,
            },
        });
    }

    /**
     * Abre el compositor de mensajes para este doctor
     * @private
     */
    _openMessageComposer() {
        const record = this.props.record.data;
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'mail.compose.message',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: {
                default_model: 'medical.doctor',
                default_res_id: record.resId,
                default_composition_mode: 'comment',
                force_email: false,
            },
        });
    }
}

class MedicalDoctorKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
    }
}

class MedicalDoctorKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.action = useService("action");
    }

    /**
     * Abre la vista de citas para un doctor específico
     * @private
     * @param {Object} record - Los datos del registro del doctor
     */
    _viewDoctorAppointments(record) {
        this.action.doAction({
            name: `Citas del Dr. ${record.data.name}`,
            type: 'ir.actions.act_window',
            res_model: 'medical.appointment',
            view_mode: 'calendar,list,form',
            domain: [['doctor_id', '=', record.resId]],
            context: {
                'default_doctor_id': record.resId,
            },
        });
    }
}

export const medicalDoctorKanbanView = {
    ...kanbanView,
    Controller: MedicalDoctorKanbanController,
    Renderer: MedicalDoctorKanbanRenderer,
    RecordComponent: MedicalDoctorKanbanRecord,
};

registry.category("views").add("medical_doctor_kanban", medicalDoctorKanbanView);