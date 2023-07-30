// main.js
import * as SimpleFunctions from './modules/simpleFunctions.js';
import * as Dashboard       from './modules/dashboard.js';
import * as PriorityNames   from './modules/priority_names.js';
import * as Config          from './modules/config.js';

export const houseId = sessionStorage.getItem('house_id');

let tareas = [];
let priorityNames = [];
let editing = false;
let tareaId = null;

export function getTareas() {
    return tareas;
}

export function setTareas(value) {
    tareas = value;
}

export function getPriorityNames() {
    return priorityNames;
}

export function setPriorityNames(value) {
    priorityNames = value;
}

export function getEditing() {
    return editing;
}

export function setEditing(value) {
    editing = value;
}

export function getTareaId() {
    return tareaId;
}

export function setTareaId(value) {
    tareaId = value;
}

// Inicializa los formularios de la aplicacion
async function initializeEventListeners() {
    Config.deleteHouseButtonEvent();

    Dashboard.taskFormSubmit(houseId);

    PriorityNames.priorityNameFormUpdate(priorityNames, houseId);
    PriorityNames.resetPriorityNamesButton();
    PriorityNames.setWeekdayNamesButton();
}

window.addEventListener('DOMContentLoaded', async () => {
    initializeEventListeners();
    
    SimpleFunctions.clearHouseIdOnLogout();
    
    // Pinta los nombres de prioridad en el selector de dashboard.html
    const taskForm = document.querySelector('#taskForm') ? document.querySelector('#taskForm') : null;
    if (taskForm) {
        await Dashboard.updatePriorityNames();
        Dashboard.updatePrioritySelect();
    }
    
    // Pinta las tareas existentes en dashboard.html
    const taskList = document.querySelector('#taskList') ? document.querySelector('#taskList') : null;
    if (taskList) {
        await Dashboard.updateTareas();
        Dashboard.renderTasks(getTareas(), getPriorityNames());
    }
});
