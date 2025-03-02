/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

/**
 * Widget personalizado para el estado de citas médicas
 */
export class AppointmentStatusBar extends Component {
    static template = "medicalbackend.AppointmentStatusBar";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.rootRef = useRef("root");
        
        this.statusOptions = [
            {value: 'scheduled', label: 'Programada', icon: 'fa-calendar', color: '#3498db'},
            {value: 'done', label: 'Realizada', icon: 'fa-check', color: '#2ecc71'},
            {value: 'canceled', label: 'Cancelada', icon: 'fa-times', color: '#e74c3c'},
            {value: 'no_show', label: 'No asistió', icon: 'fa-user-times', color: '#f39c12'}
        ];
        
        onMounted(() => this.onMounted());
    }
    
    /**
     * Configuración después del montaje del componente
     */
    onMounted() {
        if (this.props.readonly) {
            this.renderReadonly();
        } else {
            this.renderEdit();
        }
    }
    
    /**
     * Renderizar en modo solo lectura
     */
    renderReadonly() {
        const root = this.rootRef.el;
        if (!root) return;
        
        root.innerHTML = "";
        const status = this.props.value;
        const statusInfo = this.statusOptions.find(opt => opt.value === status);
        
        if (statusInfo) {
            const statusEl = document.createElement('span');
            statusEl.className = `appointment-status appointment-status-${status}`;
            statusEl.innerHTML = `<i class="fa ${statusInfo.icon}"></i> ${statusInfo.label}`;
            statusEl.style.backgroundColor = `${statusInfo.color}20`; // Color con 20% de opacidad
            statusEl.style.color = statusInfo.color;
            
            root.appendChild(statusEl);
        }
    }
    
    /**
     * Renderizar en modo edición
     */
    renderEdit() {
        const root = this.rootRef.el;
        if (!root) return;
        
        root.innerHTML = "";
        const currentStatus = this.props.value;
        
        const container = document.createElement('div');
        container.className = 'appointment-status-container';
        
        this.statusOptions.forEach(option => {
            const optionEl = document.createElement('div');
            optionEl.className = `status-option ${option.value === currentStatus ? 'selected' : ''}`;
            optionEl.dataset.value = option.value;
            optionEl.innerHTML = `<i class="fa ${option.icon}"></i> ${option.label}`;
            
            // Color personalizado si está seleccionado
            if (option.value === currentStatus) {
                optionEl.style.backgroundColor = `${option.color}20`;
                optionEl.style.color = option.color;
            }
            
            // Evento de clic para cambiar estado
            optionEl.addEventListener('click', () => {
                if (!this.props.readonly) {
                    this.props.update(option.value);
                }
            });
            
            container.appendChild(optionEl);
        });
        
        root.appendChild(container);
    }
}

// Registrar el componente en el registro de campos
registry.category("fields").add("appointment_statusbar", AppointmentStatusBar);