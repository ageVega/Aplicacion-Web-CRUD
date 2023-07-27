// main.js
import * as SimpleFunctions from './modules/simpleFunctions.js';
import * as EventForms from './modules/eventForms.js';

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

async function initializeApp() {
    EventForms.deleteHouseButtonEvent();

    EventForms.taskFormSubmit(houseId);

    EventForms.priorityNameFormUpdate(priorityNames, houseId);
    EventForms.resetPriorityNamesButton();
    EventForms.setWeekdayNamesButton();
}

window.addEventListener('DOMContentLoaded', async () => {
    initializeApp();
    
    SimpleFunctions.clearHouseIdOnLogout();
    
    const taskForm = document.querySelector('#taskForm') ? document.querySelector('#taskForm') : null;
    if (taskForm) {
        await SimpleFunctions.updatePriorityNames();
        SimpleFunctions.updatePrioritySelect();
    }
    
    const taskList = document.querySelector('#taskList') ? document.querySelector('#taskList') : null;
    if (taskList) {
        await SimpleFunctions.updateTareas();
        EventForms.renderTask(getTareas(), getPriorityNames());
    }
});
